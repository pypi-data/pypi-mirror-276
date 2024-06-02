import numbers

import numpy as np
import scipy.io as spio
from renishawWiRE import WDFReader

from . import core
from . import utils
from .preprocessing import Pipeline


def _loadmat(filename):
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)

    for key in data:
        if isinstance(data[key], spio.matlab.mat_struct):
            data[key] = _todict(data[key])

    return data


def _todict(matobj):
    """
    A recursive function which constructs from matobjects nested dictionaries.

    From: https://stackoverflow.com/questions/7008608/scipy-io-loadmat-nested-structures-i-e-dictionaries
    """
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict


def get_value(nested_dict, key):
    """
    A recursive function to get the value of a key in a nested dictionary.
    """
    for k, v in nested_dict.items():
        if k == key:
            return v
        elif isinstance(v, dict):
            p = get_value(v, key)
            if p is not None:
                return p


def witec(
        filename: str,
        *,
        preprocess: Pipeline = None,
        laser_excitation: numbers.Number = 532
) -> core.Spectrum or core.SpectralImage:
    """
    Loads MATLAB files exported from `WITec's WITec Suite software <https://raman.oxinst.com/products/software/witec-software-suite>`_.

    Parameters
    ----------
    filename : str
        The name of the MATLAB file to load. Full path or relative to working directory.
    preprocess : :class:`~ramanspy.preprocessing.Pipeline`, optional
        A preprocessing pipeline to apply to the loaded data. If not specified (default), no preprocessing is applied.
    laser_excitation : numeric, optional
        The excitation wavelength of the laser (in nm). Default is 532 nm.

    Returns
    ---------
    Union[core.Spectrum, core.SpectralImage] :
        The loaded data.

    Example
    ----------

    .. code::

        import ramanspy as rp

        # Loading a single spectrum
        raman_spectrum = rp.load.witec("path/to/file/witec_spectrum.mat")

        # Loading Raman image data
        raman_image = rp.load.witec("path/to/file/witec_image.mat")

        # Loading volumetric Raman data from a list of Raman image files by stacking them as layers along the z-axis
        image_layer_files = ["path/to/file/witec_image_1.mat", ..., "path/to/file/witec_image_n.mat"]
        raman_image_stack = [rp.load.witec(image_layer_file) for image_layer_file in image_layer_files]
        raman_volume =  rp.SpectralVolume.from_image_stack(raman_image_stack)
    """
    matlab_dict = _loadmat(filename)

    axis = get_value(matlab_dict, 'axisscale')[1]
    shift_values = utils.wavelength_to_wavenumber(axis[0], laser_excitation) if axis[1] != 'rel. 1/cm' else axis[0]

    spectral_data = get_value(matlab_dict, 'data')

    if len(spectral_data.shape) == 1:  # i.e. single spectrum
        obj = core.Spectrum(spectral_data, shift_values)

    elif len(spectral_data.shape) == 2:
        imagesize = get_value(matlab_dict, 'imagesize')
        spectral_data = spectral_data.reshape(imagesize[1], imagesize[0], -1).transpose(1, 0, 2)

        obj = core.SpectralImage(spectral_data, shift_values)

    else:
        raise ValueError(
            f"Raman Matlab type {get_value(matlab_dict, 'type')} and dimension {len(spectral_data.shape)} is unknown")

    if preprocess is not None:
        obj = preprocess.apply(obj)

    return obj


def ocean_insight(filename: str, *, preprocess: Pipeline = None, laser_excitation: numbers.Number = 532) -> core.Spectrum:
    """
    Loads spectra data from `Ocean Insight's OceanView software <https://www.oceaninsight.com/products/software/>`_ .txt files.

    Parameters
    ----------
    filename : str
        The name of the .txt file to load. Full path or relative to working directory.
    preprocess : :class:`~ramanspy.preprocessing.Pipeline`, optional
        A preprocessing pipeline to apply to the loaded data. If not specified (default), no preprocessing is applied.
    laser_excitation : numeric, optional
        The excitation wavelength of the laser (in nm). Default is 532 nm.

    Returns
    ---------
    core.Spectrum :
        The loaded data.

    Example
    ----------
    
    .. code:: 
    
        import ramanspy as rp
       
        # Loading a single spectrum
        raman_spectrum = rp.load.ocean_insight("path/to/file/ocean_insight_spectrum.txt")
    """

    region = "metadata"
    metadata = {}
    # metadata["filename"] = file_name

    data = []
    with open(filename) as f:
        for line in f:
            line = line.strip()

            if line.startswith("   >>"):
                region = "data"
                continue

            if region == "metadata":
                k, v = line.split(": ")
                metadata[k] = v
                continue

            data.append(line)

    spectral_data = data[:, 1]
    shift_values = data[:, 0]

    if metadata["XAxis mode"].lower() == "wavelengths":
        shift_values = utils.wavelength_to_wavenumber(shift_values, laser_excitation)

    spectrum = core.Spectrum(spectral_data, shift_values)

    if preprocess is not None:
        spectrum = preprocess.apply(spectrum)

    return spectrum


def renishaw(filename: str, *, preprocess: Pipeline = None) -> core.SpectralContainer or core.Spectrum or core.SpectralImage:
    """
    Loads spectra data from `Ranishaw's WiRE software <https://www.renishaw.com/en/raman-software--9450>`_ .wdf  files.

    Parameters
    ----------
    filename : str
        The name of the .wdf file to load. Full path or relative to working directory.
    preprocess : :class:`~ramanspy.preprocessing.Pipeline`, optional
        A preprocessing pipeline to apply to the loaded data. If not specified (default), no preprocessing is applied.

    Returns
    ---------
    Union[core.SpectralContainer, core.Spectrum, core.SpectralImage] :
        The loaded data.


    .. note:: Implementation based on `renishawWiRE <https://pypi.org/project/renishawWiRE/>`_.


    Example
    ----------

    .. code::

        import ramanspy as rp

        raman_spectrum = rp.load.renishaw("path/to/file/wire_data.wdf")
    """
    reader = WDFReader(filename)

    if len(reader.spectra.shape) == 1:
        obj = core.Spectrum(reader.spectra, reader.xdata)
    elif len(reader.spectra.shape) == 3:
        obj = core.SpectralImage(reader.spectra, reader.xdata)
    else:
        obj = core.SpectralContainer(reader.spectra, reader.xdata)

    if preprocess is not None:
        obj = preprocess.apply(obj)

    return obj


def opus(filename: str, *, preprocess: Pipeline = None) -> core.Spectrum:
    """
    Loads spectra data from `Bruker's OPUS software <https://www.bruker.com/en/products-and-solutions/infrared-and-raman/opus-spectroscopy-software.html>`_ files.

    Parameters
    ----------
    filename : str
        The name of the file to load. Full path or relative to working directory.
    preprocess : :class:`~ramanspy.preprocessing.Pipeline`, optional
        A preprocessing pipeline to apply to the loaded data. If not specified (default), no preprocessing is applied.

    Returns
    ---------
    core.Spectrum :
        The loaded data.


    .. warning:: The function has not been implemented yet.

    Example
    ----------

    .. code::

        import ramanspy as rp

        # Loading a single spectrum
        raman_spectrum = rp.load.opus("path/to/file/ocean_insight_spectrum.O00")
    """
    raise NotImplemented()


def labspec(filename: str, *, preprocess: Pipeline = None) -> core.SpectralContainer or core.Spectrum:
    """
    Loads spectra data from `HORIBA's LabSpec software <https://www.horiba.com/int/scientific/products/detail/action/show/Product/labspec-6-spectroscopy-suite-software-1843/>`_ .txt files.

    Parameters
    ----------
    filename : str
        The name of the .txt file to load. Full path or relative to working directory.
    preprocess : :class:`~ramanspy.preprocessing.Pipeline`, optional
        A preprocessing pipeline to apply to the loaded data. If not specified (default), no preprocessing is applied.

    Returns
    ---------
    core.SpectralContainer or core.Spectrum:
        The loaded data.


    Example
    ----------

    .. code::

        import ramanspy as rp

        # Loading Raman data from labspec
        raman_object = rp.load.labspec("path/to/file/ocean_insight_spectrum.txtO")
    """

    metadata = {}
    data = []
    with open(filename) as f:
        for line in f:
            line = line.strip()

            if line.startswith('#'):
                k, v = line.split("=")
                metadata[k] = v
                continue

            data.append(line)

    data = np.genfromtxt(data, delimiter="\t")

    if data.shape[1] == 2:
        obj = core.Spectrum(data[:, 1], data[:, 0])
    else:
        obj = core.SpectralContainer(data[1:, 1:], data[0, 1:])

    if preprocess is not None:
        obj = preprocess.apply(obj)

    return obj

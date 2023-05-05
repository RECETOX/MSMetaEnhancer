from typing import List
from matchms import Spectrum
import matchms.exporting
import matchms.importing

from MSMetaEnhancer.libs.data.Data import Data
from MSMetaEnhancer.libs.utils.Errors import UnknownSpectraFormat


class Spectra(Data):
    """
    Spectra class represents a single spectra dataset as a list.
    It is using `matchms` package to load and save MSP files.
    """
    def __init__(self):
        self.spectrums: List[Spectrum] = []

    def __eq__(self, other):
        if len(self.spectrums) == len(other.spectrums):
            return all([spectra_eq(self.spectrums[i], other.spectrums[i]) for i in range(len(self.spectrums))])
        else:
            return False

    def load_data(self, filename: str, file_format: str):
        """
        Loads given file as a list of matchms.Spectra objects.

        Supported formats: msp, mgf, json

        :param filename: given file
        :param file_format: format of the input file
        """
        self.spectrums = list(getattr(matchms.importing, f'load_from_{file_format}')(filename))

    def save_data(self, filename: str, file_format: str):
        """
        Exports all matchms.Spectra objects stored in self.spectrums to
        a file given by filename

        Supported formats: msp, mgf, json

        :param filename: target file
        :param file_format: format of the output file
        """
        try:
            getattr(matchms.exporting, f'save_as_{file_format}')(self.spectrums, filename)
        except Exception:
            raise UnknownSpectraFormat(f'Format {file_format} not supported.')

    def get_metadata(self):
        return [spectra.metadata for spectra in self.spectrums]

    def fuse_metadata(self, metadata):
        for i in range(len(metadata)):
            self.spectrums[i].metadata = metadata[i]


def spectra_eq(first: Spectrum, second: Spectrum):
    """
    Compare two Spectra objects.
    Native __eq__ definition does not work properly.

    :param first: spectra object
    :param second: spectra object
    """
    return first.peaks == second.peaks and first.losses == second.losses and first.metadata == second.metadata

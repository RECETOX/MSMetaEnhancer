from typing import List

from matchms import Spectrum
from matchms.exporting import save_as_msp
from matchms.importing import load_from_msp


class Spectra:
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

    def load_from_msp(self, filename: str):
        """
        Loads given MSP filename as a list of matchms.Spectra objects and
        stores them in self.spectrums attribute

        :param filename: given MSP file
        """
        self.spectrums = list(load_from_msp(filename))

    def save_to_msp(self, filename: str):
        """
        Exports all matchms.Spectra objects stored in self.spectrums to
        a file given by filename

        :param filename: target MSP file
        """
        save_as_msp(self.spectrums, filename)


def spectra_eq(first: Spectrum, second: Spectrum):
    """
    Compare two Spectra objects.
    Native __eq__ definition does not work properly.

    :param first: spectra object
    :param second: spectra object
    """
    return first.peaks == second.peaks and first.losses == second.losses and first.metadata == second.metadata

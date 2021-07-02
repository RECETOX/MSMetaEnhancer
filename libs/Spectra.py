from matchms.importing import load_from_msp
from matchms.exporting import save_as_msp


class Spectra:
    def __init__(self):
        self.spectrums = []

    def load_msp_file(self, filename):
        """
        Loads given MSP filename as a list of matchms.Spectra objects and
        stores them in self.spectrums attribute

        :param filename: given MSP file
        """
        self.spectrums = list(load_from_msp(filename))

    def save_msp_file(self, filename):
        """
        Exports all matchms.Spectra objects stored in self.spectrums to
        a file given by filename

        :param filename: target MSP file
        """
        save_as_msp(self.spectrums, filename)

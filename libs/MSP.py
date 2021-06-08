from matchms.importing import load_from_msp
from matchms.exporting import save_as_msp


class MSP:
    def __init__(self):
        self.spectrums = []

    def load_msp_file(self, filename):
        self.spectrums = list(load_from_msp(filename))

    def save_msp_file(self, filename):
        save_as_msp(self.spectrums, filename)

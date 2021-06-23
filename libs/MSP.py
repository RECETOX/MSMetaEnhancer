from matchms.importing import load_from_msp
from matchms.exporting import save_as_msp

from libs import curator
from libs.Annotator import Annotator


class MSP:
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

    def annotate_spectrums(self, jobs):
        """
        Adds additional metadata to all Spectra objects.

        Required metadata are specified in required_annotations attribute and
        have to be defined in and add_ method of Annotator class (otherwise ignored).

        :param jobs: target annotation jobs
        """
        annotator = Annotator()
        for i, spectrum in enumerate(self.spectrums):
            metadata = curator.curate_metadata(spectrum.metadata)
            spectrum.metadata = annotator.annotate(metadata, jobs)

    def annotate_spectrums_all_attributes(self):
        """
        Adds all implemented metadata to all Spectra objects.
        """
        annotator = Annotator()
        for i, spectrum in enumerate(self.spectrums):
            metadata = curator.curate_metadata(spectrum.metadata)
            spectrum.metadata = annotator.annotate(metadata, [], all=True)

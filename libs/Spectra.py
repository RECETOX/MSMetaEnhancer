import asyncio
import aiohttp
from matchms.importing import load_from_msp
from matchms.exporting import save_as_msp

from libs import curator
from libs.Annotator import Annotator


class Spectra:
    def __init__(self):
        self.annotator = Annotator()
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

    def get_available_jobs(self):
        """
        Method to compute all available conversion services of Annotator class.

        :return: a list of available conversion services
        """
        return self.annotator.get_all_conversions()

    async def annotate(self, jobs, batch_size, repeat):
        """
        Annotate data using specified jobs in asynchronous mode.
        Spectrums are executed in batches to avoid flooding web services.

        :param jobs: given list of jobs to do
        :param batch_size: size of single batch
        :param repeat: if some metadata was added, all jobs are executed again
        """
        async with aiohttp.ClientSession() as session:
            results = []
            for size in range(len(self.spectrums) // batch_size + 1):
                results += await asyncio.gather(*[self.annotator.annotate(spectra, jobs, session, repeat) for spectra in
                                                  self.spectrums[size * batch_size:(size + 1) * batch_size]])
        self.spectrums = results

    def annotate_spectrums(self, jobs, batch_size=10, repeat=False):
        """
        Adds additional metadata to all Spectra objects.

        Required metadata are specified in required_annotations attribute and
        have to be defined in and add_ method of Annotator class (otherwise ignored).

        :param jobs: target annotation jobs
        :param batch_size: number of spectrums annotated at once (to avoid flooding web services)
        :param repeat: if some metadata was added, all jobs are executed again
        """
        for spectrum in self.spectrums:
            spectrum.metadata = curator.curate_metadata(spectrum.metadata)
        asyncio.run(self.annotate(jobs, batch_size, repeat))

    def annotate_spectrums_all_attributes(self, batch_size=10):
        """
        Adds all implemented metadata to all Spectra objects.
        """
        jobs = self.get_available_jobs()
        self.annotate_spectrums(jobs, batch_size, True)

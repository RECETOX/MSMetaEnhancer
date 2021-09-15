class Curator:
    def curate_spectra(self, spectra):
        for spectrum in spectra.spectrums:
            spectrum.metadata = self.curate_metadata(spectrum.metadata)
        return spectra

    def curate_metadata(self, metadata):
        if 'casno' in metadata:
            metadata['casno'] = self.fix_cas_number(metadata['casno'])
        return metadata

    @staticmethod
    def fix_cas_number(cas_number):
        """
        Adds dashes to CAS number.

        :param cas_number: given CAS number
        :return: CAS number enriched by dashes (if needed)
        """
        if "-" not in cas_number:
            return f'{cas_number[:-3]}-{cas_number[-3:-1]}-{cas_number[-1]}'
        return cas_number

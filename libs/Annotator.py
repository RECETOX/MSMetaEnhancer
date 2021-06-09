from libs import converter


class Annotator:
    def __init__(self, annotations):
        self.annotations = annotations
        self.converter = converter

    def add_possible_annotations(self, metadata):
        """
        Adds additional annotations to given dictionary containing metadata

        The method goes through specified annotations and tries to invoke
        a particular method able to add required annotation.

        :param metadata: given spectra metadata
        :return: annotated dictionary
        """
        for annotation in self.annotations:
            if annotation not in metadata:
                try:
                    result = getattr(self, "add_" + annotation)(metadata)
                    if result:
                        metadata[annotation] = result
                except AttributeError:
                    pass
        return metadata

    def add_inchikey(self, metadata):
        """
        Tries to find an InChiKey based on specified metadata.

        Currently implemented strategies:
        - CTS service based on CAS number

        :param metadata: specified metadata dictionary
        :return: found InChiKey (return None if not found)
        """
        cas_number = metadata.get('casno', None)
        if cas_number:
            if "-" not in cas_number:
                cas_number = self.converter.fix_cas_number(cas_number)
            return self.converter.cas_to_inchikey(cas_number)

    def add_smiles(self, metadata):
        """
        Tries to find an SMILES based on specified metadata.

        Currently implemented strategies:
        - CIR service based on CAS number

        :param metadata: specified metadata dictionary
        :return: found SMILES (return None if not found)
        """
        cas_number = metadata.get('casno', None)
        if cas_number:
            if "-" not in cas_number:
                cas_number = self.converter.fix_cas_number(cas_number)
            return self.converter.cas_to_smiles(cas_number)

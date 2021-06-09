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

        Since some metadata might depend on other metadata which might be added
        in the process, the method iterates over the annotations until a fixpoint
        is reached.

        :param metadata: given spectra metadata
        :return: annotated dictionary
        """
        added_metadata = True
        while added_metadata:
            added_metadata = False
            for annotation in self.annotations:
                if annotation not in metadata:
                    # make sure an add method for this annotation exists
                    try:
                        result = getattr(self, "add_" + annotation)(metadata)
                        if result:
                            metadata[annotation] = result
                            added_metadata = True
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

    def add_inchi(self, metadata):
        """
        Tries to find an InChi based on specified metadata.

        Currently implemented strategies:
        - CTS compound service based on CAS InChiKey

        :param metadata: specified metadata dictionary
        :return: found InChi (return None if not found)
        """
        inchikey = metadata.get('inchikey', None)
        if inchikey:
            return self.converter.inchikey_to_inchi(inchikey)

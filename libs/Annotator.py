from libs.services.CIR import CIR
from libs.services.CTS import CTS
from libs.services.NLM import NLM


class Annotator:
    def __init__(self, annotations):
        self.annotations = annotations
        self.CTS = CTS()
        self.CIR = CIR()
        self.NLM = NLM()

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
        - CTS service based chemical name
        - NLM service based chemical name
        - CIR service based on SMILES

        :param metadata: specified metadata dictionary
        :return: found InChiKey (return None if not found)
        """
        cas_number = metadata.get('casno', None)
        if cas_number:
            inchikey = self.CTS.cas_to_inchikey(cas_number)
            if inchikey:
                return inchikey
        name = metadata.get('name', None)
        if name:
            # TODO - this is ugly
            inchikey = self.CTS.name_to_inchikey(name)
            if inchikey:
                return inchikey
            inchikey = self.NLM.name_to_inchikey(name)
            if inchikey:
                return inchikey
        smiles = metadata.get('smiles', None)
        if smiles:
            inchikey = self.CIR.smiles_to_inchikey(smiles)
            if inchikey:
                return inchikey

    def add_smiles(self, metadata):
        """
        Tries to find an SMILES based on specified metadata.

        Currently implemented strategies:
        - CIR service based on CAS number
        - CIR service based on InChiKey

        :param metadata: specified metadata dictionary
        :return: found SMILES (return None if not found)
        """
        cas_number = metadata.get('casno', None)
        if cas_number:
            smiles = self.CIR.cas_to_smiles(cas_number)
            if smiles:
                return smiles
        inchikey = metadata.get('inchikey', None)
        if inchikey:
            smiles = self.CIR.inchikey_to_smiles(inchikey)
            if smiles:
                return smiles

    def add_inchi(self, metadata):
        """
        Tries to find an InChi based on specified metadata.

        Currently implemented strategies:
        - CTS compound service based on CAS InChiKey
        - CIR service based on CAS InChiKey

        :param metadata: specified metadata dictionary
        :return: found InChi (return None if not found)
        """
        inchikey = metadata.get('inchikey', None)
        if inchikey:
            inchi = self.CTS.inchikey_to_inchi(inchikey)
            if inchi:
                return inchi
            inchi = self.CIR.inchikey_to_inchi(inchikey)
            if inchi:
                return inchi

    def add_name(self, metadata):
        """
        Tries to find an Chemical name based on specified metadata.

        Currently implemented strategies:
        - CTS service based on InChiKey
        - NLM service based on InChiKey

        :param metadata: specified metadata dictionary
        :return: found Chemical name (return None if not found)
        """
        inchikey = metadata.get('inchikey', None)
        if inchikey:
            name = self.CTS.inchikey_to_name(inchikey)
            if name:
                return name
            name = self.NLM.inchikey_to_name(inchikey)
            if name:
                return name

    def add_IUPAC(self, metadata):
        """
        Tries to find an IUPAC name based on specified metadata.

        Currently implemented strategies:
        - CTS service based on InChiKey

        :param metadata: specified metadata dictionary
        :return: found IUPAC name (return None if not found)
        """
        inchikey = metadata.get('inchikey', None)
        if inchikey:
            iupac_name = self.CTS.inchikey_to_IUPAC_name(inchikey)
            if iupac_name:
                return iupac_name

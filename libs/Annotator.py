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
        a particular method able to add required annotation (keyword is skipped
        if such method does not exist).

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
                        result = getattr(self, f"add_{annotation}")(metadata)
                        if result:
                            metadata[annotation] = result
                            added_metadata = True
                    except AttributeError:
                        pass
        return metadata

    @staticmethod
    def execute_conversions(conversions, metadata):
        """
        General method to execute provided alternative ways how to obtain specific metadata.

        Parameter conversions has format {metadata_key: [methods], ...}.
        Provided methods require metadata_key as an input argument and
        are used to obtain target metadata.

        :param conversions: given methods to execute
        :param metadata: specified metadata dictionary
        :return: obtained target attribute (None if not found)
        """
        for metadata_key in conversions:
            metadata_value = metadata.get(metadata_key, None)
            if metadata_value:
                for method in conversions[metadata_key]:
                    result = method(metadata_value)
                    if result:
                        return result

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
        conversions = {'casno': [self.CTS.cas_to_inchikey],
                       'name': [self.CTS.name_to_inchikey, self.NLM.name_to_inchikey],
                       'smiles': [self.CIR.smiles_to_inchikey]}
        return self.execute_conversions(conversions, metadata)

    def add_smiles(self, metadata):
        """
        Tries to find an SMILES based on specified metadata.

        Currently implemented strategies:
        - CIR service based on CAS number
        - CIR service based on InChiKey

        :param metadata: specified metadata dictionary
        :return: found SMILES (return None if not found)
        """
        conversions = {'casno': [self.CIR.cas_to_smiles],
                       'inchikey': [self.CIR.inchikey_to_smiles]}
        return self.execute_conversions(conversions, metadata)

    def add_inchi(self, metadata):
        """
        Tries to find an InChi based on specified metadata.

        Currently implemented strategies:
        - CTS compound service based on CAS InChiKey
        - CIR service based on CAS InChiKey

        :param metadata: specified metadata dictionary
        :return: found InChi (return None if not found)
        """
        conversions = {'inchikey': [self.CTS.inchikey_to_inchi, self.CIR.inchikey_to_inchi]}
        return self.execute_conversions(conversions, metadata)

    def add_name(self, metadata):
        """
        Tries to find an Chemical name based on specified metadata.

        Currently implemented strategies:
        - CTS service based on InChiKey
        - NLM service based on InChiKey

        :param metadata: specified metadata dictionary
        :return: found Chemical name (return None if not found)
        """
        conversions = {'inchikey': [self.CTS.inchikey_to_name, self.NLM.inchikey_to_name]}
        return self.execute_conversions(conversions, metadata)

    def add_IUPAC(self, metadata):
        """
        Tries to find an IUPAC name based on specified metadata.

        Currently implemented strategies:
        - CTS service based on InChiKey

        :param metadata: specified metadata dictionary
        :return: found IUPAC name (return None if not found)
        """
        conversions = {'inchikey': [self.CTS.inchikey_to_IUPAC_name, self.NLM.inchikey_to_name]}
        return self.execute_conversions(conversions, metadata)

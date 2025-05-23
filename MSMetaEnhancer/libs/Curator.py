from matchms.filtering.filter_utils.smile_inchi_inchikey_conversions import (
    is_valid_smiles, is_valid_inchi, is_valid_inchikey
)

# Example usage
smiles = "C1=CC=CC=C1"
inchi = "InChI=1S/CH4/h1H4"
inchikey = "VNWKTOKETHGBQD-UHFFFAOYSA-N"

print(is_valid_smiles(smiles))  # True if valid SMILES
print(is_valid_inchi(inchi))    # True if valid InChI
print(is_valid_inchikey(inchikey))  # True if valid InChIKey
from MSMetaEnhancer.libs.utils.Errors import InvalidAttributeFormat


class Curator:
    """
    Curator makes sure that all data is curated before the actual annotation can proceed.
    Currently, fixing CAS numbers to correct format is supported.

    Additionally, it supports metadata validation to make sure the produced data are correct.
    """
    def curate_metadata(self, metadata_list):
        """
        Iterates over given metadata and curates individual entries.

        :param metadata_list: given metadata
        :return: curated metadata
        """
        curated_metadata_list = []
        for metadata in metadata_list:
            curated_metadata_list.append(self.curate_casno(metadata))
        return curated_metadata_list

    def curate_casno(self, metadata):
        """
        Curate metadata of particular spectra.

        :param metadata: given metadata
        :return: curated metadata
        """
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
        if isinstance(cas_number, str):
            if "-" not in cas_number:
                return f'{cas_number[:-3]}-{cas_number[-3:-1]}-{cas_number[-1]}'
        return cas_number

    @staticmethod
    def filter_invalid_metadata(metadata, log, job):
        """
        Validates metadata and filters out invalid ones.

        :param metadata: metadata content
        :param log: object storing logs related to current metadata
        :param job: executed job
        :return: only valid metadata
        """
        filters = {
            'smiles': is_valid_smiles,
            'canonical_smiles': is_valid_smiles,
            'isomeric_smiles': is_valid_smiles,
            'inchi': is_valid_inchi,
            'inchikey': is_valid_inchikey
        }

        valid_metadata = {}
        for (attribute, value) in metadata.items():
            if attribute in filters.keys():
                if filters[attribute](value):
                    valid_metadata[attribute] = value
                else:
                    log.update(InvalidAttributeFormat(f'Obtained {attribute} in invalid format: {value}'), job, level=2)
            else:
                valid_metadata[attribute] = value
        return valid_metadata

from rdkit.Chem.Descriptors import ExactMolWt
from rdkit.Chem import MolFromSmiles

from MSMetaEnhancer.libs.converters.compute.ComputeConverter import ComputeConverter


class RDKit(ComputeConverter):
    """
    RDKit is a collection of cheminformatics and machine-learning software.
    """
    def __init__(self):
        super().__init__()
        # generate top level methods defining allowed conversions
        conversions = [('smiles', 'mw', 'from_smiles'),
                       ('canonical_smiles', 'mw', 'from_smiles'),
                       ('isomeric_smiles', 'mw', 'from_smiles')]
        self.create_top_level_conversion_methods(conversions, asynch=False)

    def from_smiles(self, smiles):
        weight = ExactMolWt(MolFromSmiles(smiles))
        return {'mw': weight}

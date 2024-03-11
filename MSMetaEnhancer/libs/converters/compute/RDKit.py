import re
from rdkit.Chem.Descriptors import ExactMolWt
from rdkit.Chem import MolFromSmiles, MolToSmiles
from rdkit.Chem.inchi import MolFromInchi
from rdkit.Chem import Atom


from MSMetaEnhancer.libs.converters.compute.ComputeConverter import ComputeConverter


class RDKit(ComputeConverter):
    """
    RDKit is a collection of chemo-informatics and machine-learning software.
    """
    def __init__(self):
        super().__init__()
        # generate top level methods defining allowed conversions
        conversions = [('smiles', 'mw', 'from_smiles'),
                       ('canonical_smiles', 'mw', 'from_smiles'),
                       ('isomeric_smiles', 'mw', 'from_smiles')]
        self.create_top_level_conversion_methods(conversions, asynch=False)

    def from_smiles(self, smiles):
        """
        Compute molecular exact weight from SMILES.

        :param smiles: given SMILES
        :return: computed molecular weight
        """
        weight = ExactMolWt(MolFromSmiles(smiles))
        return {'mw': weight}

    def inchi_to_canonical_smiles(self, inchi):
        """
        Compute canonical SMILES from InChI.

        :param inchi: given InChI
        :return: computed canonical SMILES
        """
        smiles = MolToSmiles(MolFromInchi(inchi), isomericSmiles=False)
        return {'canonical_smiles': smiles}

    def inchi_to_isomeric_smiles(self, inchi):
        """
        Compute isomeric SMILES from InChI.

        :param inchi: given InChI
        :return: computed isomeric SMILES
        """
        smiles = MolToSmiles(MolFromInchi(inchi))
        return {'isomeric_smiles': smiles}

    def formula_to_mw(self, formula):
        """
        Compute molecular exact weight from molecular formula.

        :param smiles: given SMILES
        :return: computed molecular weight
        """
        parts = re.findall("[A-Z][a-z]?|[0-9]+", formula)
        mass = 0

        for index in range(len(parts)):
            if parts[index].isnumeric():
                continue

            atom = Atom(parts[index])
            multiplier = int(parts[index + 1]) if len(parts) > index + 1 and parts[index + 1].isnumeric() else 1
            mass += atom.GetMass() * multiplier
        return {'mw': mass}

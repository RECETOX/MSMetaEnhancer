from abc import ABC, abstractmethod
from typing import List, Dict


class Data(ABC):
    """
    General class for data.
    """
    @abstractmethod
    def get_metadata(self) -> List[Dict]:
        """
        Returns a list of dictionaries containing metadata for annotation.

        :return: metadata in form of list of dictionaries
        """
        pass

    def fuse_metadata(self, metadata: List[Dict]):
        """
        Fuse updated metadata back to its original format.

        :param metadata:
        """
        pass

import pandas

from MSMetaEnhancer.libs.data.Data import Data


class DataFrame(Data):
    def __init__(self):
        self.df = pandas.DataFrame()

    def load_from_csv(self, filename):
        """
        Loads metadata from CSV file and stores them in pandas DataFrame.

        :param filename: given CSV file
        """
        self.df = pandas.read_csv(filename, dtype=str)

    def save_to_csv(self, filename):
        """
        Store metadata as a table to given CSV file.

        :param filename: target CSV file
        """
        self.df.to_csv(filename, index=False)

    def get_metadata(self):
        return self.df.to_dict('records')

    def fuse_metadata(self, metadata_list):
        self.df = pandas.DataFrame.from_dict(metadata_list)

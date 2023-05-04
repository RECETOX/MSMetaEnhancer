import pandas

from MSMetaEnhancer.libs.data.Data import Data


class DataFrame(Data):
    def __init__(self):
        self.df = pandas.DataFrame()

    def load_from_csv(self, filename, sep=','):
        """
        Loads metadata from CSV file and stores them in pandas DataFrame.

        :param filename: given CSV file
        :param sep: data separator
        """
        self.df = pandas.read_csv(filename, dtype=str, sep=sep)

    def load_from_tsv(self, filename):
        """
        Loads metadata from TSV file and stores them in pandas DataFrame.

        :param filename: given TSV file
        """
        self.load_from_csv(filename, sep='\t')

    def load_from_xlsx(self, filename):
        """
        Loads metadata from Excel sheet and stores them in pandas DataFrame.

        :param filename: given xlsx file
        """
        self.df = pandas.read_excel(filename, dtype=str)

    def save_to_csv(self, filename, sep=','):
        """
        Store metadata as a table to given CSV file.

        :param filename: target CSV file
        :param sep: data separator
        """
        self.df.to_csv(filename, index=False, sep=sep)

    def save_to_tsv(self, filename):
        """
        Store metadata as a table to given TSV file.

        :param filename: target TSV file
        """
        self.save_to_csv(filename, sep='\t')

    def save_to_xlsx(self, filename):
        """
        Store metadata as an Excel sheet.

        :param filename: target Excel sheet
        """
        self.df.to_excel(filename)

    def get_metadata(self):
        return self.df.to_dict('records')

    def fuse_metadata(self, metadata_list):
        self.df = pandas.DataFrame.from_dict(metadata_list)

import pandas

from MSMetaEnhancer.libs.data.Data import Data
from MSMetaEnhancer.libs.utils.Errors import UnknownFileFormat


class DataFrame(Data):
    def __init__(self):
        self.df = pandas.DataFrame()

    def load_data(self, filename: str, file_format: str):
        """
        Loads given file as a list of pandas DataFrame.

        Supported formats: csv, tsv/tabular, xlsx

        :param filename: given file
        :param file_format: format of the input file
        """
        if file_format == 'csv':
            self.df = pandas.read_csv(filename, dtype=str)
        elif file_format in ['tsv', 'tabular']:
            self.df = pandas.read_csv(filename, dtype=str, sep='\t')
        elif file_format == 'xlsx':
            self.df = pandas.read_excel(filename, dtype=str)
        else:
            raise UnknownFileFormat(f'Format {file_format} not supported.')

    def save_data(self, filename: str, file_format: str):
        """
        Exports DataFrame stored a file given by filename

        Supported formats: csv, tsv, xlsx

        :param filename: target file
        :param file_format: format of the output file
        """
        if file_format == 'csv':
            self.df.to_csv(filename, index=False)
        elif file_format in ['tsv', 'tabular']:
            self.df.to_csv(filename, index=False, sep='\t')
        elif file_format == 'xlsx':
            self.df.to_excel(filename)
        else:
            raise UnknownFileFormat(f'Format {file_format} not supported.')

    def get_metadata(self):
        return self.df.to_dict('records')

    def fuse_metadata(self, metadata_list):
        self.df = pandas.DataFrame.from_dict(metadata_list)

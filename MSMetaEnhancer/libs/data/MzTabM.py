import csv

from MSMetaEnhancer.libs.data.Data import Data
from MSMetaEnhancer.libs.utils.Errors import UnknownFileFormat
from MSMetaEnhancer.libs.utils.Generic import is_na_value


class MzTabM(Data):
    """
    Data backend for the small molecule summary section of mzTab-M files.
    """

    COLUMN_ALIASES = {
        "chemical_formula": "formula",
        "chemical_name": "compound_name",
        "inchi_key": "inchikey",
    }

    @classmethod
    def normalize_column(cls, column):
        column = column.removeprefix("opt_")
        return cls.COLUMN_ALIASES.get(column, column)

    def __init__(self):
        self.file_rows = []
        self.header_index = None
        self.data_indices = []
        self.header = []
        self.metadata = []

    def load_data(self, filename: str, file_format: str = "mztab-m"):
        """
        Loads small molecule metadata from an mzTab-M file.

        :param filename: path to the input file
        :param file_format: format of the input file
        """
        if file_format not in ["mztab-m", "mztab_m", "mztabm"]:
            raise UnknownFileFormat(f"Format {file_format} not supported.")

        with open(filename, encoding="utf-8", newline="") as file:
            self.file_rows = list(csv.reader(file, delimiter="\t"))

        self.header_index = None
        self.data_indices = []
        self.header = []
        self.metadata = []

        for index, row in enumerate(self.file_rows):
            if not row:
                continue
            if row[0] == "SMH":
                self.header_index = index
                self.header = row[1:]
            elif row[0] == "SML":
                if self.header_index is None:
                    raise ValueError("mzTab-M SML row found before its SMH header.")
                if len(row) != len(self.header) + 1:
                    raise ValueError("mzTab-M SML row does not match its SMH header.")
                self.data_indices.append(index)
                self.metadata.append(
                    {
                        self.normalize_column(column): value
                        for column, value in zip(self.header, row[1:])
                        if not is_na_value(value) and value.strip().lower() != "null"
                    }
                )

    def get_metadata(self):
        return [record.copy() for record in self.metadata]

    def fuse_metadata(self, metadata):
        if len(metadata) != len(self.data_indices):
            raise ValueError("Metadata length does not match mzTab-M SML rows.")

        aliases = {value: key for key, value in self.COLUMN_ALIASES.items()}
        header_lookup = {column: index + 1 for index, column in enumerate(self.header)}

        for row_index, record in zip(self.data_indices, metadata):
            row = self.file_rows[row_index]
            for key, value in record.items():
                column = aliases.get(key, key)
                column_index = header_lookup.get(column)
                if column_index is None:
                    column = f"opt_{key}"
                    column_index = header_lookup.get(column)
                    if column_index is None:
                        self.header.append(column)
                        self.file_rows[self.header_index].append(column)
                        header_lookup[column] = len(self.header)
                        column_index = header_lookup[column]
                while len(row) <= column_index:
                    row.append("")
                row[column_index] = str(value)
        self.metadata = [record.copy() for record in metadata]

    def save_data(self, filename: str, file_format: str = "mztab-m"):
        """
        Writes the mzTab-M document, including any fused metadata.

        :param filename: path to the output file
        :param file_format: format of the output file
        """
        if file_format not in ["mztab-m", "mztab_m", "mztabm"]:
            raise UnknownFileFormat(f"Format {file_format} not supported.")

        with open(filename, "w", encoding="utf-8", newline="") as file:
            csv.writer(file, delimiter="\t", lineterminator="\n").writerows(
                self.file_rows
            )

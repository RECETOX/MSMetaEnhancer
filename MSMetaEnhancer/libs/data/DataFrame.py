import pandas


class DataFrame:
    def __init__(self):
        self.df = pandas.DataFrame()

    def load_from_csv(self, filename):
        self.df = pandas.read_csv(filename, dtype=str)

    def save_to_csv(self, filename):
        self.df.to_csv(filename, index=False)

    def get_metadata(self):
        return self.df.to_dict('records')

    def fuse_metadata(self, metadata_list):
        self.df = pandas.DataFrame.from_dict(metadata_list)

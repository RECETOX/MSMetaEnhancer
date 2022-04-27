from tabulate import tabulate


class Metrics:
    def __init__(self):
        self.coverage_before_annotation = dict()
        self.coverage_after_annotation = dict()
        self.max_spectra = 0

    def set_params(self, target_attributes, length):
        """
        Set all parameters needed to compute metrics.

        :param target_attributes: target attributes to be obtained during annotation
        :param length: number of spectra data
        """
        self.coverage_before_annotation = {key: 0 for key in target_attributes}
        self.coverage_after_annotation = {key: 0 for key in target_attributes}
        self.max_spectra = length

    def update_before_annotation(self, metadata_keys):
        """
        Increase counts of already present attributes.

        :param metadata_keys: present attributes
        """
        for key in self.coverage_before_annotation:
            if key in metadata_keys:
                self.coverage_before_annotation[key] += 1

    def update_after_annotation(self, metadata_keys):
        """
        Increase counts of annotated attributes

        :param metadata_keys: discovered attributes
        """
        for key in self.coverage_after_annotation:
            if key in metadata_keys:
                self.coverage_after_annotation[key] += 1

    def __str__(self):
        table = tabulate([[key,
                           f'{(self.coverage_before_annotation[key]/self.max_spectra)*100:.2f}%',
                           f'{(self.coverage_after_annotation[key]/self.max_spectra)*100:.2f}%']
                          for key in self.coverage_before_annotation],
                         headers=['Target\nattribute', 'Coverage\nbefore', 'Coverage\nafter'])

        return f'\nAttribute discovery rates:\n\n{table}\n' + '='*50 + '\n'

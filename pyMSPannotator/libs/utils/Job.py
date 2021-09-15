from pyMSPannotator.libs.utils.Errors import ConversionNotSupported, SourceAttributeNotAvailable


class Job:
    def __init__(self, data):
        self.source, self.target, self.service = data

    def __str__(self):
        return f'{self.service}: {self.source} -> {self.target}'

    def __repr__(self):
        return f'Job(({self.source}, {self.target}, {self.service}))'

    def validate(self, services, metadata):
        service = services.get(self.service, None)
        data = metadata.get(self.source, None)

        if service is None:
            raise ConversionNotSupported(f'Conversion ({self.service}) {self.source} -> {self.target}: is not supported')
        elif data is None:
            raise SourceAttributeNotAvailable(f'Conversion ({self.service}) {self.source} -> {self.target}: '
                                              f'Attribute {self.source} missing in given metadata.')
        else:
            return service, data


def convert_to_jobs(jobs):
    return [Job(data) for data in jobs]

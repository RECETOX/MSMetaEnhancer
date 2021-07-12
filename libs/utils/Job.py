from libs.utils.Errors import ConversionNotSupported, DataNotAvailable


class Job:
    def __init__(self, data):
        self.source, self.target, self.service = data

    def __str__(self):
        return f'{self.source} -> {self.target} : {self.service}'

    def __repr__(self):
        return f'Job(({self.source}, {self.target}, {self.service}))'

    def validate(self, services, metadata):
        service = services.get(self.service, None)
        data = metadata.get(self.source, None)

        if service is None:
            raise ConversionNotSupported(f'Specified {service} not supported.')
        elif data is None:
            raise DataNotAvailable(f'Source {self.source} not available in metadata.')
        else:
            return service, data


def convert_to_jobs(jobs):
    return [Job(data) for data in jobs]

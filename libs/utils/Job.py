class Job:
    def __init__(self, data):
        self.source, self.target, self.service = data

    def __str__(self):
        return f'{self.source} -> {self.target} : {self.service}'

    def __repr__(self):
        return f'Job(({self.source}, {self.target}, {self.service}))'


def convert_to_jobs(jobs):
    return [Job(data) for data in jobs]

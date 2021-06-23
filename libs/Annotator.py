from libs.utils.Errors import ConversionNotSupported, DataNotRetrieved
from libs.services.CIR import CIR
from libs.services.CTS import CTS
from libs.services.NLM import NLM
from libs.services.PubChem import PubChem


class Annotator:
    def __init__(self, jobs):
        self.jobs = jobs
        self.services = {'CTS': CTS(), 'CIR': CIR(), 'NLM': NLM(), 'PubChem': PubChem()}

    def annotate(self, metadata):
        """
        Runs all jobs to add annotations to given dictionary containing metadata

        The method goes through specified jobs of form (Source, Target, Service)
        and tries to obtain 'Target' attribute based on 'Source' attribute using
        'Service' service.

         TODO: run only once or until fixpoint is reached?

        :param metadata: given spectra metadata
        :return: annotated dictionary
        """
        for job in self.jobs:
            service = self.services.get(job.service, None)
            if service:
                data = metadata.get(job.source, None)
                if data:
                    try:
                        result = service.convert(job.source, job.target, data)
                        metadata[job.target] = result
                    except ConversionNotSupported as e:
                        pass  # TODO log this type of conversion is not supported by the service
                    except DataNotRetrieved as e:
                        pass  # TODO log no data were retrieved
                else:
                    pass
                    # TODO: log data not available for conversion
            else:
                pass
                # TODO: log unknown service
        return metadata
    
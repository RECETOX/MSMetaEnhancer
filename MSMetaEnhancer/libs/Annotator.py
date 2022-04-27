import traceback

from MSMetaEnhancer.libs.Curator import Curator
from MSMetaEnhancer.libs.utils import logger
from MSMetaEnhancer.libs.utils.Errors import TargetAttributeNotRetrieved, SourceAttributeNotAvailable, \
    ServiceNotAvailable, UnknownResponse, DataAlreadyPresent
from MSMetaEnhancer.libs.utils.Logger import LogRecord


class Annotator:
    """
    Annotator is responsible for annotation process of single spectra.
    """
    def __init__(self):
        self.converters = dict()
        self.curator = Curator()

    def set_converters(self, converters):
        self.converters = converters

    async def annotate(self, spectra, jobs, repeat=False):
        """
        Runs all jobs to add annotations to given dictionary containing metadata

        The method goes through specified jobs of form (Source, Target, Converter)
        and tries to obtain 'Target' attribute based on 'Source' attribute using
        'Converter' converter.

        :param spectra: given spectra metadata
        :param jobs: specified list of jobs to be executed
        :param repeat: if some metadata was added, all jobs are executed again
        :return: annotated dictionary
        """
        metadata = spectra.metadata
        cache = dict()
        log = LogRecord(dict(metadata))
        logger.add_coverage_before(metadata.keys())

        added_metadata = True
        while added_metadata:
            added_metadata = False
            for job in jobs:
                if job.target not in metadata:
                    try:
                        metadata, cache = await self.execute_job_with_cache(job, metadata, cache, log)
                        if repeat:
                            added_metadata = True
                    except (SourceAttributeNotAvailable, TargetAttributeNotRetrieved) as exc:
                        log.update(exc, job, level=3)
                    except (ServiceNotAvailable, UnknownResponse) as exc:
                        log.update(exc, job, level=2)
                    except Exception:
                        log.update(Exception(traceback.format_exc()), job, level=1)
                else:
                    log.update(DataAlreadyPresent(f'Requested attribute {job.target} already present.'), job, level=2)

        logger.add_logs(log)
        logger.add_coverage_after(metadata.keys())

        spectra.metadata = metadata
        return spectra

    async def execute_job_with_cache(self, job, metadata, cache, warning):
        """
        Execute given job in cached mode. Cache is converter specific
        and spectra specific.

        Raises TargetAttributeNotRetrieved

        :param job: given job to be executed
        :param metadata: data to be annotated by the job
        :param cache: given cache for this spectra
        :param warning: object storing warnings related to current metadata
        :return: updated metadata and cache
        """
        # make sure the job makes sense
        converter, data = job.validate(self.converters, metadata)

        cache[job.converter] = cache.get(job.converter, dict())
        if job.target in cache[job.converter]:
            metadata[job.target] = cache[job.converter][job.target]
        else:
            if converter.is_available:
                result = await converter.convert(job.source, job.target, data)
                result = self.curator.filter_invalid_metadata(result, warning, job)
                cache[job.converter].update(result)
                if job.target in cache[job.converter]:
                    metadata[job.target] = cache[job.converter][job.target]
                else:
                    raise TargetAttributeNotRetrieved(f'No data retrieved.')
            else:
                raise ServiceNotAvailable(f'Service {job.converter} not available.')
        return metadata, cache

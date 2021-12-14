from MSMetaEnhancer.libs.utils import logger
from MSMetaEnhancer.libs.utils.Errors import ConversionNotSupported, TargetAttributeNotRetrieved, \
    SourceAttributeNotAvailable, ServiceNotAvailable, UnknownResponse
from MSMetaEnhancer.libs.utils.Logger import LogWarning
from MSMetaEnhancer.libs.utils.Monitor import Monitor


class Annotator:
    def __init__(self, services):
        self.services = services
        self.monitor = Monitor(self.services)
        self.monitor.start()

    async def annotate(self, spectra, jobs, repeat=False):
        """
        Runs all jobs to add annotations to given dictionary containing metadata

        The method goes through specified jobs of form (Source, Target, Service)
        and tries to obtain 'Target' attribute based on 'Source' attribute using
        'Service' service.

        :param spectra: given spectra metadata
        :param jobs: specified list of jobs to be executed
        :param repeat: if some metadata was added, all jobs are executed again
        :return: annotated dictionary
        """
        metadata = spectra.metadata
        cache = dict()
        warning = LogWarning(dict(metadata))
        logger.add_coverage_before(metadata.keys())

        added_metadata = True
        while added_metadata:
            added_metadata = False
            for job in jobs:
                if job.target not in metadata:
                    try:
                        metadata, cache = await self.execute_job_with_cache(job, metadata, cache)
                        if repeat:
                            added_metadata = True
                    except (ConversionNotSupported, TargetAttributeNotRetrieved, UnknownResponse) as exc:
                        warning.add_warning(exc)
                    except SourceAttributeNotAvailable as exc:
                        warning.add_info(exc)
                    except ServiceNotAvailable:
                        warning.add_warning(ServiceNotAvailable(f'Service {job.service} not available.'))
                else:
                    warning.add_info(f'Conversion ({job.service}) {job.source} -> {job.target}: Requested '
                                     f'attribute {job.target} already present in given metadata.')

        logger.add_warning(warning)
        logger.add_coverage_after(metadata.keys())

        spectra.metadata = metadata
        return spectra

    async def execute_job_with_cache(self, job, metadata, cache):
        """
        Execute given job in cached mode. Cache is service specific
        and spectra specific.

        Raises TargetAttributeNotRetrieved

        :param job: given job to be executed
        :param metadata: data to be annotated by the job
        :param cache: given cache for this spectra
        :return: updated metadata and cache
        """
        # make sure the job makes sense
        service, data = job.validate(self.services, metadata)

        cache[job.service] = cache.get(job.service, dict())
        if job.target in cache[job.service]:
            metadata[job.target] = cache[job.service][job.target]
        else:
            if service.is_available:
                result = await service.convert(job.source, job.target, data)
                cache[job.service].update(result)
                if job.target in cache[job.service]:
                    metadata[job.target] = cache[job.service][job.target]
                else:
                    raise TargetAttributeNotRetrieved('No data obtained from the specified job.')
            else:
                raise ServiceNotAvailable
        return metadata, cache

    def exit(self):
        self.monitor.join()

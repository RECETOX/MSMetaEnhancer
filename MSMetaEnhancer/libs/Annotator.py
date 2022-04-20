from MSMetaEnhancer.libs.Curator import Curator
from MSMetaEnhancer.libs.utils import logger
from MSMetaEnhancer.libs.utils.Errors import ConversionNotSupported, TargetAttributeNotRetrieved, \
    SourceAttributeNotAvailable, ServiceNotAvailable, UnknownResponse, UnknownError
from MSMetaEnhancer.libs.utils.Logger import LogWarning


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
        warning = LogWarning(dict(metadata))
        logger.add_coverage_before(metadata.keys())

        added_metadata = True
        while added_metadata:
            added_metadata = False
            for job in jobs:
                if job.target not in metadata:
                    try:
                        metadata, cache = await self.execute_job_with_cache(job, metadata, cache, warning)
                        if repeat:
                            added_metadata = True
                    except (ConversionNotSupported, TargetAttributeNotRetrieved, UnknownResponse) as exc:
                        warning.add_warning(exc)
                    except SourceAttributeNotAvailable as exc:
                        warning.add_info(exc)
                    except ServiceNotAvailable:
                        warning.add_warning(ServiceNotAvailable(f'Service {job.converter} not available.'))
                    except Exception as e:
                        logger.error(UnknownError(e))
                else:
                    warning.add_info(f'Conversion ({job.converter}) {job.source} -> {job.target}: Requested '
                                     f'attribute {job.target} already present in given metadata.')

        logger.add_warning(warning)
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
                    raise TargetAttributeNotRetrieved(f'{job} - conversion retrieved no data.')
            else:
                raise ServiceNotAvailable
        return metadata, cache

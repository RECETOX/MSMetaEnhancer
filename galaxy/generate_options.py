import sys
import os

# this add to path the home dir, so it can be called from anywhere
sys.path.append(os.path.split(sys.path[0])[0])

from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder

from MSMetaEnhancer.libs.converters.web import __all__ as web_converters
from MSMetaEnhancer.libs.converters.compute import __all__ as compute_converters


def generate_options():
    ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])

    jobs = []
    converters = web_converters + compute_converters

    builder = ConverterBuilder()
    builder.validate_converters(converters)
    built_compute_converters, built_web_converters = builder.build_converters(
        None, converters
    )

    for converter in built_compute_converters.values():
        jobs += converter.get_conversion_functions()

    for converter in built_web_converters.values():
        jobs += converter.get_conversion_functions()

    for job in jobs:
        print(
            f'<option value="{job[0]} {job[1]} {job[2]}">{job[2]}: {job[0]} -> {job[1]}</option>'
        )


if __name__ == "__main__":
    generate_options()

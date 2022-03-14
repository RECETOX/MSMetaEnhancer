import sys
import os

# this add to path the home dir, so it can be called from anywhere
sys.path.append(os.path.split(sys.path[0])[0])

from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.converters.web import __all__ as web_converters
from MSMetaEnhancer.libs.converters.compute import __all__ as compute_converters


def generate_options():
    jobs = []
    converters = web_converters + compute_converters
    built_converters, built_web_converters = ConverterBuilder().build_converters(None, converters)

    for converter in built_converters:
        jobs += (built_converters[converter].get_conversion_functions())

    for job in jobs:
        print(f'<option value="{job[0]} {job[1]} {job[2]}">{job[2]}: {job[0]} -> {job[1]}</option>')


if __name__ == '__main__':
    generate_options()

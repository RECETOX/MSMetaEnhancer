import sys
import os

# this add to path the home dir, so it can be called from anywhere
sys.path.append(os.path.split(sys.path[0])[0])

from MSMetaEnhancer.libs.services import *
from MSMetaEnhancer.libs.services import __all__ as services


def generate_options():
    jobs = []
    for service in services:
        jobs += (eval(service)(None).get_conversion_functions())

    for job in jobs:
        print(f'<option value="{job[0]} {job[1]} {job[2]}">{job[2]}: {job[0]} -> {job[1]}</option>')


if __name__ == '__main__':
    generate_options()

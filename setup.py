from setuptools import setup, find_packages


def read_requirements_from_file(filepath):
    with open(filepath, 'r') as req_file:
        return req_file.readlines()


setup_args = dict(
    install_requires=read_requirements_from_file('requirements.txt'),
    tests_require=read_requirements_from_file('requirements-dev.txt')
)


with open("README.md") as readme_file:
    readme = readme_file.read()

setup(name='MSMetaEnhancer',
      version='0.2.4',
      description='Repository for tool that adds more annotations '
                  '(e.g. SMILES, InChI, CAS number) to MSP files (Python version).',
      long_description=readme,
      long_description_content_type="text/markdown",
      url='https://github.com/RECETOX/MSMetaEnhancer',
      author='Matej Trojak',
      author_email='matej.trojak@recetox.muni.cz',
      maintainer="RECETOX",
      maintainer_email="GalaxyToolsDevelopmentandDeployment@space.muni.cz",
      license='MIT',
      packages=find_packages(exclude=['*tests*']),
      zip_safe=False,
      test_suite="tests",
      python_requires='>=3.7',
      install_requires=setup_args['install_requires'],
      extras_require={'test': setup_args['tests_require']},
      )

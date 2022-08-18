from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(name='MSMetaEnhancer',
      version='0.2.3',
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
      install_requires=[
            "matchms",
            "requests",
            "pandas",
            "aiohttp",
            "asyncstdlib",
            "frozendict",
            "tabulate",
            "aiocircuitbreaker"
      ],
      extras_require={
        'test': [
            'pytest',
            'pytest-cov'
        ]
      },
      )

from setuptools import setup, find_packages

setup(name='MSMetaEnhancer',
      version='0.2',
      description='Repository for tool that adds more annotations '
                  '(e.g. SMILES, InChI, CAS number) to MSP files (Python version).',
      url='https://github.com/RECETOX/MSMetaEnhancer',
      author='Matej Trojak',
      author_email='matej.trojak@recetox.muni.cz',
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
            "tabulate"
      ]
      )

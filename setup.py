from setuptools import setup

setup(name='pyMSPannotator',
      version='0.1',
      description='Repository for tool that adds more annotations '
                  '(e.g. SMILES, InChI, CAS number) to MSP files (Python version).',
      url='https://github.com/RECETOX/pyMSPannotator',
      author='Matej Trojak',
      author_email='matej.trojak@recetox.muni.cz',
      license='MIT',
      packages=['pyMSPannotator'],
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
      ],
      )

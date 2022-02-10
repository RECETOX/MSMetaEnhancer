# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [dev] - unreleased
### Added
* multidict package requirement
* tracking of attributes validation in log [#68](https://github.com/RECETOX/MSMetaEnhancer/issues/68)
* CIR: Inchi -> SMILES conversion [#66](https://github.com/RECETOX/MSMetaEnhancer/issues/66)
### Changed
* passed `multidict` instead of `frozendict` to `aiohttp.ClientSession.post` (required by package)
* take only first result when there are multiple hits in CIR conversions [#69](https://github.com/RECETOX/MSMetaEnhancer/issues/69)
* support `ISOMERIC_SMILES` and `CANONICAL_SMILES` in PubChem instead of generic `SMILES` [#67](https://github.com/RECETOX/MSMetaEnhancer/issues/67)
### Removed

## [0.1.2] - 2022-01-06
### Added
- `generate_options()` function in `Galaxy` submodule to create all possible conversions supported by the tool in a format suitable for the galaxy tool form [#58](https://github.com/RECETOX/MSMetaEnhancer/pull/58)
- monitoring of services status during annotation process [#56](https://github.com/RECETOX/MSMetaEnhancer/issues/56)
- validation of obtained metadata [#59](https://github.com/RECETOX/MSMetaEnhancer/issues/59)
### Changed
- structure and contents of documentation [#51](https://github.com/RECETOX/MSMetaEnhancer/pull/51)
### Removed
- tests checking contents and consistency of individual services [#54](https://github.com/RECETOX/MSMetaEnhancer/pull/61)

## [0.1.1] - 2021-12-07
### Added
- `get_conversion_functions` on the level of `Converter`
### Changed
- computation of all available jobs in `Application`
### Removed
- `get_all_conversions` on the level of `Annotator`

## [0.1.0] - 2021-11-16
### Added
- Added conda environment files [#35](https://github.com/RECETOX/MSMetaEnhancer/pull/35)
- Usage of IDSM SPARQL for PubChem service [#25](https://github.com/RECETOX/MSMetaEnhancer/pull/25)
- Added logging and quantitative progress of annotation process [#22](https://github.com/RECETOX/MSMetaEnhancer/pull/22)
- Generalised requests to obtain multiple values at once [#20](https://github.com/RECETOX/MSMetaEnhancer/pull/20)
- Added asynchronous requests [#15](https://github.com/RECETOX/MSMetaEnhancer/pull/15)

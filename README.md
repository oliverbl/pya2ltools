# PyA2LTools

This is a collection of tools to work with [A2L files](https://www.asam.net/standards/detail/mcd-2-mc/wiki/).


* Reads A2L files up to Version 1.71 into a Python datastructure
* Writes A2L files from a Python datastructure
* Can be used to progamatically modify A2L files (for example merging multuple a2l files, remvoving elements, etc.)

Tested with the ECU Description File from [ASAM](https://www.asam.net/index.php?eID=dumpFile&t=f&f=2132&token=1672c6611f14141ae705140149a9401141821de0)

I do not have access to the standard, so there will be some missing features. If you find any bugs or missing features, please open an issue.


## Comparison with pyA2L

pya2ltools reads the file into a python native datastructure using dataclasses. It does not require knowledge about accessing a DB.
The tool was written with the newest version available (1.71)

I tried to minimize the external dependencies. It does not use a Language Parser Library, instead the parser is written by hand.
Also writing the A2L file is done by standard python methods. (Allthough a templating engine like Jinja2 could be used)

## Updating ECU Adresses
(WIP)

[Pyelftools](https://github.com/eliben/pyelftools) is used to parse an ELF File and extract the addresses of the symbols. In the future the addresses will be updated in the A2L file.

## User Interface

Currently there is no User Interface. In the future there will be a CLI.
At the moment the tools can be used as a library.

## License

Licensed under [GNU General Public License v3.0](COPYING)
from setuptools import setup

name = "types-netaddr"
description = "Typing stubs for netaddr"
long_description = '''
## Typing stubs for netaddr

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`netaddr`](https://github.com/drkjam/netaddr) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`netaddr`.

This version of `types-netaddr` aims to provide accurate annotations
for `netaddr==1.3.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/netaddr. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `c82d29fc7614a9ecd33bd416386062ba2915850d` and was tested
with mypy 1.10.0, pyright 1.1.364, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="1.3.0.20240530",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/netaddr.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['netaddr-stubs'],
      package_data={'netaddr-stubs': ['__init__.pyi', 'cli.pyi', 'compat.pyi', 'contrib/__init__.pyi', 'contrib/subnet_splitter.pyi', 'core.pyi', 'eui/__init__.pyi', 'eui/ieee.pyi', 'fbsocket.pyi', 'ip/__init__.pyi', 'ip/glob.pyi', 'ip/iana.pyi', 'ip/nmap.pyi', 'ip/rfc1924.pyi', 'ip/sets.pyi', 'strategy/__init__.pyi', 'strategy/eui48.pyi', 'strategy/eui64.pyi', 'strategy/ipv4.pyi', 'strategy/ipv6.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

# Sphinx-OdtParser
OdtParser allows to include odt(libreoffice) files in sphinx-doc.

## Installation 
1. Install pandoc.
   >See: https://pandoc.org/
2. Install sphinx-doc
   >See: bin/initdev.cmd
3. Copy src/sphinx_odtparser in a directory which is include in PYTHONPATH

## Add OdtParser
Add following in the config.py:
```
from sphinx_odtparser.OdtParser import OdtParser
def setup(app):
    app.add_source_parser(OdtParser)
    app.add_source_suffix(".bodt","bodt")
```

see: testdoc/source/conf.py

## Include odt files in build 
1. Save some file in the source directory.
2. Create the build marker in the same directory
   >It is the file with the same name and "bodt" extension
4. Add build marker to toc
   >See: source/test_cases/index.rst
   
## Autobuild 
See: bin/autobuild.cmd
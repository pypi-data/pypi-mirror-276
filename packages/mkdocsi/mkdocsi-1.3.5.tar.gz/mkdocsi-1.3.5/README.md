# mkdocsi : 

## Why  : 
consider you have nested folders that have makrdown documentation and want tool that convert them to website dynamiccly build the sute map urls according to path to url .



## Installation : 
```bash
pip install mkdocsi
```

## Quick start : 
all agumenst passed are optionnals  : 
```bash
python -m mkdocsi --docs=./docs --index=./README.md --site_name=documentation --mkdocs=./mkdocs.yml
```
when it come to doc repo git its handy to consider README.md as home page and have `docs` folder have all makdown files 

```bash
mkdocsi --docs=./docs --index=./README.md 
```
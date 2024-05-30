# IATI Sphinx Theme

## Development

### Install dependencies

```
pip install -r requirements_dev.txt
```

### Update dependencies

```
python -m piptools compile --extra=dev -o requirements_dev.txt pyproject.toml
pip install -r requirements_dev.txt
```

### Run linting

```
black iati_sphinx_theme/
isort iati_sphinx_theme/
flake8 iati_sphinx_theme/
mypy iati_sphinx_theme/
```

### Documentation with live preview

1. In one terminal, build the CSS in watch mode

   ```
   npm run build:watch
   ```

2. In a separate terminal, install the Sphinx theme then start the docs development server:

   ```
   pip install -e .
   sphinx-autobuild -a docs docs/_build/html --watch iati_sphinx_theme/
   ```

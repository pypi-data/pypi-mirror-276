# Python packaging

Based on this guide: https://packaging.python.org/en/latest/tutorials/packaging-projects/


## Pushing new update

You will need to have `build` and `twine` installed:

```
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
```

1. Update the code and commit
2. Update the version in `pyproject.toml` and commit
3. Build the project by `python3 -m build`
4. Upload the built files in the `dist/*` folder to PyPi by `python3 -m twine upload dist/*`
    1. Username is `__token__`
    2. Password is the upload token from PyPi
5. Done, now the package can be downloaded by people

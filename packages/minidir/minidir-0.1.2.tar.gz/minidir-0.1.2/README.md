# minidir: Minimal directory interface and implementation

The minimal interface for directories and files and
two implementations: in-memory and real file system versions.

## Development

Local (editable) installation is required before running tests.

```shell
pip install -e .
```


---

## Create API token for CLI upload

- Goto <https://pypi.org/manage/account/token/>
- Create token
- Save token in `$HOME/.pypirc`
    - username: `__token__`
    - password: `pypi-some-token`


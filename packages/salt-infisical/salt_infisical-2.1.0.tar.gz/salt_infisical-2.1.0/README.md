# salt-infisical

[![PyPI - Version](https://img.shields.io/pypi/v/salt-infisical.svg)](https://pypi.org/project/salt-infisical)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/salt-infisical.svg)](https://pypi.org/project/salt-infisical)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
salt-pip install salt-infisical
echo "[your infisical token]" > /etc/salt/infisical.token
```

## Usage

Add a pillar file for every infisical folder you want to fetch:

```python
#!py
def run():
    from salt_infisical import fetch_infisical_secrets
    return fetch_infisical_secrets("prod", "/some/path")
```



## License

`salt-infisical` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

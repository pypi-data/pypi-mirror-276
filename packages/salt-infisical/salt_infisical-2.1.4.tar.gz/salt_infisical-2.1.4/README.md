# salt-infisical

[![PyPI - Version](https://img.shields.io/pypi/v/salt-infisical.svg)](https://pypi.org/project/salt-infisical)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/salt-infisical.svg)](https://pypi.org/project/salt-infisical)

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```bash
salt-pip install salt-infisical
echo '{ client_id: "[your client id]", client_secret: "[your client secret], project_id: "[your project id, can be overridden per-pillar]" }' > /etc/salt/infisical_config.json
```

***IMPORTANT: salt-infisical versions >= 2.0.0 only work with machine identities, for use with service tokens (deprecated) you can use versions < 2.0.0***

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

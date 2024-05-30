# Cherwell API Client

![Tests badge](https://github.com/dan-smalley/CherwellAPIClient/actions/workflows/test_and_lint.yml/badge.svg) 
[![Documentation Status](https://readthedocs.org/projects/cherwellapiclient/badge/?version=latest)](https://cherwellapiclient.readthedocs.io/en/latest/?badge=latest) 
![PyPI - Version](https://img.shields.io/pypi/v/CherwellAPIClient?logo=pypi&label=PyPI)
![GitHub Release](https://img.shields.io/github/v/release/dan-smalley/CherwellAPIClient?include_prereleases&logo=github&label=Release)
![TestPyPI - Version](https://img.shields.io/pypi/v/CherwellAPIClient?pypiBaseUrl=https%3A%2F%2Ftest.pypi.org&logo=pypi&label=TestPyPI) 

> NOTE: This module is inspired by the excellent [ZenossAPIClient](https://github.com/Zuora-TechOps/ZenossAPIClient) by Zuora-TechOps and the [fork](https://github.com/boblickj/ZenossAPIClient) contributed by boblickj.
> 
> My own fork of that project is available via [PyPI as zenAPIClient](https://pypi.org/project/zenAPIClient/) 
> 
>-dan-smalley

Python module for interacting with the Cherwell API in an object-oriented way.
Tested with API version 10.1.0, no guarantees for earlier versions...

The philosophy here is to use objects to work with everything in the Cherwell API, and to try to normalize the various calls to the different routers.
Thus `get` methods will always return an object, `list` methods will return data.
All methods to add or create start with `add`, all remove or delete start with `delete`.
As much as possible the methods try to hide the idiosyncrasies of the JSON API, and to do the work for you, for example by letting you use a device name instead of having to provide the full device UID for every call.

## Installing

```
pip install CherwellAPIClient
```

## Using

```
In [1]: from cherwellapi import apiclient as capi

In [2]: cherwell_client = capi.Client(host=CHERWELL_URL, client_id=CLIENT_ID, username=USERNAME, passwrod=PASSWORD)

```

Simple API client for Yandex Cloud
=========================

Status
======

This package is currently in **beta** status. It means the API may still change
in **backwards incompatible** way.

Installation
============

```
$ pip install TBA
```

Configuration
=============

You need [OAuth token](https://cloud.yandex.ru/docs/iam/concepts/authorization/oauth-token) (static, lifetime 1 year) and [IAM token](https://cloud.yandex.ru/docs/iam/concepts/authorization/iam-token) (dynamically created through OAuth token, valid for no more than 12 hours).     

Usage
=====

Import the `ycloud` package:

```python
import ycloud
```

Create an `API` instance using authentication with OAuth token:

```python
auth = ycloud.SimpleAuth('your-oauth-token')
api = ycloud.API(auth)
```

Send request using components:

```python
response = api.vision.batchAnalyze(data)
```
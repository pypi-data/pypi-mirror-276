## English

# aioasterisk
Async Asterisk Client

Python 3.6+

## Install

```bash
pip install aioasterisk
```

## Auth

First you need gen auth url:
```python
from aioasterisk.ami import AMIClient

client = AMIClient(address='127.0.0.1',port=5038)
client.login(username='username',secret='password')
```

# wxhandler

A Python package for handling wxHandler operations. it will be use on wechat-3.9.2.23. Take it for open http server or tcp server and do something.

## Installation

```bash
pip install wxhandler
```
## Usage
```python
from wxhandler import wxHandler

handler = wxHandler(base_url="http://127.0.0.1:19088") 
handler.hookSyncMsgNew(enableHttp=True, httpPort=19099) 
```



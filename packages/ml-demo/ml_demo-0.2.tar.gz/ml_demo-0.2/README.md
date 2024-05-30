# ml_demo
ml_demo是操作异步打印hello并能打印环境变量path的值库

## 用法
```python

import asyncio

from core.ml_core import async_msg, get_utils_log

get_utils_log()
asyncio.run(async_msg())

```

## 场景
1.用于异步打印hello
2.打印path
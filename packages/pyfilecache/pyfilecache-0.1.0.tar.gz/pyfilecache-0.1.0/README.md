# pyfilecache

```py
import pandas as pd
from functools import partial
from pyfilecache import file_cache

df_cache = partial(file_cache, reader=pd.read_csv, writer=pd.DataFrame.to_csv)

@df_cache
def func(a, b):
    print(a, b)
    return pd.DataFrame(
        data = {
            'col1': [1, 2],
            'col2': [a, b]
        }
    )

print(func(3, 4))
```
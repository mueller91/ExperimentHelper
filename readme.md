## A helper for setting up ML experiments

Supports
- Multiprocessing with pathos
- Automatic save and load in a nice way
- logging

### Example
```python
from main import ExpHelper
import time

def single_loop(a, b):
    def func_expensive(a, b):
        time.sleep(1)
        str(a) + str(b)
    e.do_or_load('data_store', ['a', 'b'], func_expensive, {'a': a, 'b': b})

settings = {'a': [1, 2, 3], 'b': ['hu', 'hi', 'ho']}
e = ExpHelper(name='e0', settings=settings)
e.parallelize(single_loop, ['a', 'b'])
```
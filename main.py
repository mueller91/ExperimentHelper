import itertools
import os
import time
from typing import Union
from datetime import datetime

import logging
import dill
import pathos as pathos

logging.basicConfig(
    # filename='HISTORYlistener.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class ExpHelper:
    def __init__(self, name, settings: dict):
        self.name = name
        self.settings = settings

    def parallelize(self, function, on_settings_keys: list, cpu_p=0.8):
        def logfun(*args):
            logging.info(msg="Start run with" + str(args))
            return function(*args)

        for s in on_settings_keys:
            assert s in self.settings.keys(), f"{s} not in settings (keys: {' '.join(self.settings.keys())})"
        mp = pathos.helpers.mp
        p = mp.Pool(int(cpu_p * os.cpu_count()))
        return p.starmap(logfun, itertools.product(*[self.settings[i] for i in on_settings_keys]))

    @staticmethod
    def do_or_load(base_path, list_of_properties, func, args: dict):

        def custom_path(max_len=None):
            max_len = len(list_of_properties) if max_len is None else max_len
            return [f"{j}={args[j]}" for j in list_of_properties[:max_len]]

        fname = 'store.dill'
        path_of_file = os.path.join(base_path, *custom_path(), fname)
        if os.path.exists(path_of_file):
            with open(path_of_file, 'rb') as df:
                return dill.load(df)

        # if not exists:
        res = func(**args)
        for i in range(len(list_of_properties) + 1):
            p = os.path.join(base_path, *custom_path(i))
            if not os.path.exists(p):
                os.mkdir(p)
        with open(path_of_file, 'wb') as df:
            dill.dump(res, df)

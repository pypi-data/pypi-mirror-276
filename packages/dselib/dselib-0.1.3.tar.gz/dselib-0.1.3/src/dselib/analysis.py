# -*- coding: utf-8 -*-
import os 


import pandas as pd
import numpy as np




# 컬럼당 유니크 밸류
def view_unique_values(df):
    columns = list(df.columns)
    print()
    data = []
    for c in columns:
        vals = list(df[c].unique())
        data.append({'column': c, 'unq_len': len(vals), 'sample': vals[:50]})

        if len(vals) > 100:
            print(f'{c} --> {len(vals)} | {vals[:100]}')
        else:
            print(f'{c} --> {len(vals)} | {vals}')
    
    return pd.DataFrame(data).sort_values('unq_len', ascending=False).reset_index(drop=True)






# -*- coding: utf-8 -*-
import json 
import os 

import pandas as pd


import ipylib2

from dselib import fileio


def generate_summary_csv(read_dir, write_dir):
    jsons = ipylib2.ifile.get_files(read_dir, type='json', fullpath=True)
    data = []
    print('\n\n')
    for file in sorted(jsons):
        print('PATH:', file)
        js = ipylib2.ifile.read_json(file)
        # print('JSON:', js)
        pipe_name = js['pipeline']['name']
        # print('PIPELINE:', pipe_name)
        path = js['pipeline']['config']['dataflow']['filter']['prefix']
        # print('STORAGE_PATH:', path)
        # break
        data.append({'pipeline_name': pipe_name, 'source_file': path})
    
    df = pd.DataFrame(data)
    csv_file = os.path.join(write_dir, "DataPipelineRelations.csv")
    fileio.save_as_csv(csv_file, df)

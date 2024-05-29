# -*- coding: utf-8 -*-
import os 
import sys 
import subprocess
from datetime import datetime


import requests


from ipylib.idebug import *





DECODE_KEY = "PAv0rpbn9m83ILzwbzerJiMreB9ShjY34j23xlhCmq2WFN0ZUxCwiTKQ5UZXxU0erBl/m074t1QKXlZpVI86nQ=="


def __reqGet__(url, params):
    params.update({'serviceKey': DECODE_KEY})
    try:
        response = requests.get(url, params=params)
    except requests.ConnectionError as e:
        logger.error([e, url, params])

        filepath = os.path.realpath(os.environ['RUN_FILE_PATH'])
        subprocess.run([sys.executable, filepath] + sys.argv[1:])
    finally:
        return response
    

def _inputTradeMonth(value):
    if value is None:
        return datetime.now().astimezone().strftime('%Y%m')
    else:
        return value
    

"""국토교통부_아파트매매 실거래 상세 자료"""
@tracer.info
def getRTMSDataSvcAptTradeDev(locationCode, tradeMonth=None, n_rows='1000'):
    url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
    tradeMonth = _inputTradeMonth(tradeMonth)
    params ={'pageNo' : '1', 'numOfRows' : n_rows, 'LAWD_CD' : locationCode, 'DEAL_YMD' : tradeMonth }
    res = __reqGet__(url, params)
    return _handle_response(res)
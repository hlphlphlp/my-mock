#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : HLP
# @File : main.py
# @Date : 2020/6/10 
# @Desc :
import time
from mock_server import add_route, start_server

if __name__ == '__main__':
    add_route(url='/hello', response={"hello": "world"})

    add_route(url='/gcm/send', method='POST', response={
                                           "multicast_id": 8507328404259215356,
                                           "success": 1,
                                           "failure": 0,
                                           "canonical_ids": 0,
                                            "results": [
                                               {
                                                  "message_id": "0:1430983178997591%921c249af9fd7ecd"
                                               }
                                            ]
                                         })
    add_route(url='/v1/pas/send', method='POST', response={})
    start_server()
    time.sleep(3000)
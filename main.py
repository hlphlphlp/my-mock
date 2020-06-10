#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : HLP
# @File : main.py
# @Date : 2020/6/10 
# @Desc :
import time
from mock_server import add_route, start_server

if __name__ == '__main__':
    add_route(url='/v1/books/', response=[{'id': 1}], method='GET')
    add_route(url='/', response={})
    add_route(url='/hello', response={"hello": "world"})
    start_server()
    time.sleep(300)
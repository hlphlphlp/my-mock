#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : HLP
# @File : main.py
# @Date : 2020/6/10
# @Desc :

from mock_server import add_route, app

add_route(url='/hello', response={"hello": "world"})
# FCM
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
}, status_code=200)
add_route(url='/v1/pas/send', method='POST', response={})
# MTS
add_route(url='/imsi', method='GET', response={}, status_code=504)

add_route(url='/ses/pushserver/notifyPushTokenCleanup', method='POST', response={"errorCode": "GD-01-008",
                                                                                 "message": "Stale profile cleanup service failed: RequestPromiseError: deleteRegistration request fails!"},
          status_code=500)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True)

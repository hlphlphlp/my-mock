#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : HLP
# @File : my_mock_server.py
# @Date : 2020/6/9 
# @Desc :

import os
import json
import threading
from typing import Optional, Dict, Callable, Any
from helpers import json_safe, semiflatten, get_url, get_headers, get_files

from flask import Flask, jsonify, request

mock_box_dict = {}

app = Flask(__name__)

def add_route(url: str,
              response: Optional[str] = None,
              method: str = 'GET',
              response_type: str = 'JSON',
              status_code: int = 200,
              headers: Optional[Dict[str, str]] = None,
              callback: Optional[Callable[[Any], None]] = None,
              ) -> None:
    """
    Add route to app.
    :param url: the URL rule as string
    :param response: return value
    :param method: HTTP method
    :param response_type: type of response (JSON, HTML, RSS)
    :param status_code: return status code
    :param headers: return headers
    :param callback: function will be executes before response returns
    """
    mock_box_dict[url] = []
    endpoint = '{url}::{method}::{status_code}'.format(
        url=url, method=method, status_code=status_code
    )

    @app.route(url, endpoint=endpoint, methods=[method])
    def handler(*args, **kwargs):
        if callback is not None:
            callback(request, *args, **kwargs)
        json_response = jsonify(response)
        if headers is not None:
            json_response.headers.update(headers)
        if request.method == 'GET':
            request_dict = get_dict("url", "args", "headers", "origin")
            mock_box_dict[url].append(request_dict)
        else:
            request_dict = get_dict("url", "args", "form", "data", "origin", "headers", "files", "json")
            mock_box_dict[url].append(request_dict)
        print(json.dumps(request_dict))
        return json_response, status_code


def get_dict(*keys, **extras):
    """Returns request dict of given keys."""

    _keys = ('url', 'args', 'form', 'data', 'origin', 'headers', 'files', 'json', 'method')

    assert all(map(_keys.__contains__, keys))
    data = request.data
    form = semiflatten(request.form)

    try:
        _json = json.loads(data.decode('utf-8'))
    except (ValueError, TypeError):
        _json = None

    d = dict(
        url=get_url(request),
        args=semiflatten(request.args),
        form=form,
        data=json_safe(data),
        origin=request.headers.get('X-Forwarded-For', request.remote_addr),
        headers=get_headers(),
        files=get_files(),
        json=_json,
        method=request.method,
    )

    out_d = dict()

    for key in keys:
        out_d[key] = d.get(key)

    out_d.update(extras)

    return out_d


def start_server(host='0.0.0.0', port=5000):
    thread = threading.Thread(target=app.run(host=host, port=port), daemon=True)
    thread.start()
    return thread


def pytest_configure(config):
    config.addinivalue_line('markers', 'server: mark test to run mock server')


def pytest_runtest_setup(item):
    markers = list(item.iter_markers('server'))
    print(markers)
    if len(markers) > 0:
        os.environ['WERKZEUG_RUN_MAx`IN'] = 'true'
        for marker in markers:
            add_route(*marker.args, **marker.kwargs)
        start_server()


@app.route('/clearMockBox', methods=['DELETE'])
def clear_mock_box():
    if isinstance(request.get_json(force=True), list):
        url_list = request.get_json()
    else:
        return "The format must be a list", 400

    for url in url_list:
        mock_box_dict[url] = []
    return jsonify(url_list), 200


@app.route('/getMockBox')
def get_mock_box():
    if request.args:
        if request.args['url'] in mock_box_dict.keys():
            return jsonify(mock_box_dict[request.args['url']])
        else:
            return "This URL does not exist", 400
    return jsonify(mock_box_dict)


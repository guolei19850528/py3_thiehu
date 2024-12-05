#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_tiehu
=================================================
"""
import hashlib
import json
from datetime import datetime

import requests
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response


class Pklot(object):
    def __init__(
            self,
            base_url: str = "",
            parking_id: str = "",
            app_key: str = ""
    ):
        base_url = base_url if isinstance(base_url, str) else ""
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base_url = base_url
        self.parking_id = parking_id if isinstance(parking_id, str) else ""
        self.app_key = app_key if isinstance(app_key, str) else ""

    def _default_response_handler(self, response: Response = None):
        """
        default response handler
        :param response: requests.Response instance
        :return:
        """
        if isinstance(response, Response) and response.status_code == 200:
            json_addict = Dict(response.json())
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "status": {
                        "oneOf": [
                            {"type": "integer", "const": 1},
                            {"type": "string", "const": "1"},
                        ]
                    },
                },
                "required": ["status", "Data"]
            }).is_valid(json_addict):
                return json.loads(json_addict.get("Data", "")), response
        return False, response

    def signature(
            self,
            data: dict = None,
    ):
        temp_string = ""
        data = data if isinstance(data, dict) else {}
        if data.keys():
            data_sorted = sorted(data.keys())
            if isinstance(data_sorted, list):
                temp_string = "&".join([
                    f"{i}={data[i]}"
                    for i in
                    data_sorted if
                    i != "appKey"
                ]) + f"{hashlib.md5(self.app_key.encode('utf-8')).hexdigest().upper()}"
        return hashlib.md5(temp_string.encode('utf-8')).hexdigest().upper()

    def request_with_signature(
            self,
            method: str = "POST",
            url: str = None,
            **kwargs
    ):
        """
        request with signature
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else ""
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        kwargs.setdefault("json", {})
        kwargs["json"] = {
            **{
                "parkingId": self.parking_id,
                "timestamp": int(datetime.now().timestamp()),
                "sign": self.signature({
                    "parkingId": self.parking_id,
                    "timestamp": int(datetime.now().timestamp()),
                })
            },
            **kwargs["json"],
        }
        response = requests.request(method=method, url=url, **kwargs)
        return self._default_response_handler(response)

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

class UrlSettings:
    CXZN_INTERFACE_QUERYPKLOT = "/cxzn/interface/queryPklot"
    CXZN_INTERFACE_GETPARKCARTYPE = "/cxzn/interface/getParkCarType"
    CXZN_INTERFACE_GETPARKCARMODEL = "/cxzn/interface/getParkCarModel"
    CXZN_INTERFACE_PAYMONTHLY = "/cxzn/interface/payMonthly"
    CXZN_INTERFACE_ADDVISIT = "/cxzn/interface/addVisit"
    CXZN_INTERFACE_LOCKCAR = "/cxzn/interface/lockCar"
    CXZN_INTERFACE_GETPARKINFO = "/cxzn/interface/getParkinfo"
    CXZN_INTERFACE_ADDPARKBLACK = "/cxzn/interface/addParkBlack"
    CXZN_INTERFACE_DELPARKBLACKLIST = "/cxzn/interface/delParkBlacklist"
    CXZN_INTERFACE_GETPARKGATE = "/cxzn/interface/getParkGate"
    CXZN_INTERFACE_OPENGATE = "/cxzn/interface/openGate"
    CXZN_INTERFACE_SAVEMONTHLYRENT = "/cxzn/interface/saveMonthlyRent"
    CXZN_INTERFACE_DELMONTHLYRENT = "/cxzn/interface/delMonthlyRent"
    CXZN_INTERFACE_GETMONTHLYRENT = "/cxzn/interface/getMonthlyRent"
    CXZN_INTERFACE_GETMONTHLYRENTLIST = "/cxzn/interface/getMonthlyRentList"
    CXZN_INTERFACE_DELMONTHLYRENTLIST = "/cxzn/interface/delMonthlyRentList"
    CXZN_INTERFACE_GETPARKDEVICESTATE = "/cxzn/interface/getParkDeviceState"
    CXZN_INTERFACE_UPATEPLATEINFO = "/cxzn/interface/upatePlateInfo"
    CXZN_INTERFACE_GETPARKBLACKLIST = "/cxzn/interface/getParkBlackList"
    CXZN_INTERFACE_DELETEVISITT = "/cxzn/interface/deleteVisit"


class Pklot(object):
    """
    @see https://www.showdoc.com.cn/1735808258920310/9467753400037587
    """

    def __init__(
            self,
            base_url: str = "",
            parking_id: str = "",
            app_key: str = ""
    ):
        """
        @see https://www.showdoc.com.cn/1735808258920310/9467753400037587
        :param base_url:
        :param parking_id:
        :param app_key:
        """
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
                return Dict(json.loads(json_addict.get("Data", ""))), response
        return False, response

    def signature(
            self,
            data: dict = None,
    ):
        """
        @see https://www.showdoc.com.cn/1735808258920310/8113601111753119
        :param data:
        :return:
        """
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
        timestamp = int(datetime.now().timestamp())
        kwargs.setdefault("json", {})
        kwargs["json"] = {
            **{
                "parkingId": self.parking_id,
                "timestamp": timestamp,
                "sign": self.signature({
                    "parkingId": self.parking_id,
                    "timestamp": timestamp,
                })
            },
            **kwargs["json"],
        }
        response = requests.request(method=method, url=url, **kwargs)
        return self._default_response_handler(response)

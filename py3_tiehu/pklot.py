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

import py3_requests
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response


class RequestUrl:
    QUERYPKLOT_URL = "/cxzn/interface/queryPklot"
    GETPARKCARTYPE_URL = "/cxzn/interface/getParkCarType"
    GETPARKCARMODEL_URL = "/cxzn/interface/getParkCarModel"
    PAYMONTHLY_URL = "/cxzn/interface/payMonthly"
    ADDVISIT_URL = "/cxzn/interface/addVisit"
    LOCKCAR_URL = "/cxzn/interface/lockCar"
    GETPARKINFO_URL = "/cxzn/interface/getParkinfo"
    ADDPARKBLACK_URL = "/cxzn/interface/addParkBlack"
    DELPARKBLACKLIST_URL = "/cxzn/interface/delParkBlacklist"
    GETPARKGATE_URL = "/cxzn/interface/getParkGate"
    OPENGATE_URL = "/cxzn/interface/openGate"
    SAVEMONTHLYRENT_URL = "/cxzn/interface/saveMonthlyRent"
    DELMONTHLYRENT_URL = "/cxzn/interface/delMonthlyRent"
    GETMONTHLYRENT_URL = "/cxzn/interface/getMonthlyRent"
    GETMONTHLYRENTLIST_URL = "/cxzn/interface/getMonthlyRentList"
    DELMONTHLYRENTLIST_URL = "/cxzn/interface/delMonthlyRentList"
    GETPARKDEVICESTATE_URL = "/cxzn/interface/getParkDeviceState"
    UPATEPLATEINFO_URL = "/cxzn/interface/upatePlateInfo"
    GETPARKBLACKLIST_URL = "/cxzn/interface/getParkBlackList"
    DELETEVISITT_URL = "/cxzn/interface/deleteVisit"


class ValidatorJsonSchema:
    """
    json schema settings
    """
    NORMAL_SCHEMA = {
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
    }


class ResponseHandler:
    """
    response handler
    """

    @staticmethod
    def normal_handler(response: Response = None):
        if isinstance(response, Response) and response.status_code == 200:
            json_addict = Dict(response.json())
            if Draft202012Validator(ValidatorJsonSchema.NORMAL_SCHEMA).is_valid(instance=json_addict):
                return Dict(json.loads(json_addict.get("Data", "")))
            return None
        raise Exception(f"Response Handler Error {response.status_code}|{response.text}")


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

        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.parking_id = parking_id
        self.app_key = app_key

    def signature(
            self,
            data: dict = {},
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
            **kwargs
    ):
        """
        request with signature
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("response_handler", ResponseHandler.normal_handler)
        kwargs.setdefault("url", f"")
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.setdefault("json", Dict())
        timestamp = int(datetime.now().timestamp())
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
        return py3_requests.request(
            **kwargs.to_dict()
        )

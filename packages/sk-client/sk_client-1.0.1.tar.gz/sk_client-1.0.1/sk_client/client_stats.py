#!/usr/bin/python3

from http import HTTPStatus
from typing import List

from requests import Response

from sk_schemas.stats import API_STATS_V1, FileDataModel, StatsStringModel

from .client_base import HttpClient


class ClientStatsMgr:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def get_hw_stats(self, iface_name=None) -> tuple[Response, StatsStringModel | None]:

        iface_ep = ""
        if iface_name:
            iface_ep = f"/{iface_name}"

        resp = self.http_client.http_get(API_STATS_V1 + "/hw" + iface_ep)

        if resp and resp.status_code == HTTPStatus.OK:
            stats_json = resp.json()
            return resp, StatsStringModel(**stats_json)

        return resp, None

    def get_ipsec_stats(self) -> tuple[Response, StatsStringModel | None]:

        resp = self.http_client.http_get(API_STATS_V1 + "/ipsec")

        if resp and resp.status_code == HTTPStatus.OK:
            stats_json = resp.json()
            return resp, StatsStringModel(**stats_json)

        return resp, None

    def get_error_stats(
        self,
    ) -> tuple[Response, StatsStringModel | None]:

        resp = self.http_client.http_get(API_STATS_V1 + "/errors")

        if resp and resp.status_code == HTTPStatus.OK:
            stats_json = resp.json()
            return resp, StatsStringModel(**stats_json)

        return resp, None

    def get_crypto_stats(self) -> tuple[Response, List[FileDataModel]]:

        resp = self.http_client.http_get(API_STATS_V1 + "/crypto")

        resp_list = []
        if resp and resp.status_code == HTTPStatus.OK:
            data = resp.json()
            for k in data:
                resp_list.append(FileDataModel(**k))
        return resp, resp_list

#!/usr/bin/python3


import json
from http import HTTPStatus
from ipaddress import IPv4Network
from typing import List

from requests import Response

from sk_schemas.acl import API_ACL_V1, AclAction, IpAclRule, IpProtocol, MacIpAclRule
from sk_schemas.intf import IfaceRoleTypes

from .client_base import HttpClient


class ClientAclMgr:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def get_acl_rules(
        self,
    ) -> tuple[Response, list[IpAclRule]]:
        resp = self.http_client.http_get(API_ACL_V1 + "/rules/ip")
        ret_list = []
        if resp and resp.status_code == HTTPStatus.OK:
            for dict in resp.json():
                ret_list.append(IpAclRule(**dict))
            return resp, ret_list
        return resp, []

    def add_acl_rule(
        self,
        rule: IpAclRule,
    ) -> Response:
        data = json.loads(rule.model_dump_json())

        resp = self.http_client.http_post(API_ACL_V1 + "/rules/ip", json=data)
        return resp

    def set_acl_rules(
        self,
        rules: List[IpAclRule],
    ) -> Response:
        data = []
        for r in rules:
            data.append(json.loads(r.model_dump_json()))

        resp = self.http_client.http_put(API_ACL_V1 + "/rules/ip", json=data)
        return resp

    def set_macip_rules(
        self,
        rules: List[MacIpAclRule],
    ) -> Response:
        data = []
        for r in rules:
            data.append(json.loads(r.model_dump_json()))

        resp = self.http_client.http_put(API_ACL_V1 + "/rules/macip", json=data)
        return resp

    def delete_acl_rule(
        self,
        rule: IpAclRule,
    ) -> Response:
        data = json.loads(rule.model_dump_json())

        resp = self.http_client.http_delete(API_ACL_V1 + "/rules/ip", json=data)
        return resp

    def delete_all_acl_rules(self) -> Response:
        # delete all acl rules using a set with an empty list
        return self.set_acl_rules([])

    def delete_all_macip_rules(self) -> Response:
        # delete all rules using a set with an empty list
        return self.set_macip_rules([])

    def get_macip_acl_rules(
        self,
    ) -> tuple[Response, list[MacIpAclRule]]:
        resp = self.http_client.http_get(API_ACL_V1 + "/rules/macip")
        ret_list = []
        if resp and resp.status_code == HTTPStatus.OK:
            for dict in resp.json():
                ret_list.append(MacIpAclRule(**dict))
            return resp, ret_list
        return resp, []

    def add_macip_acl_rule(
        self,
        rule: MacIpAclRule,
    ) -> Response:
        data = json.loads(rule.model_dump_json())

        resp = self.http_client.http_post(API_ACL_V1 + "/rules/macip", json=data)
        return resp

    def delete_macip_acl_rule(
        self,
        rule: MacIpAclRule,
    ) -> Response:
        data = json.loads(rule.model_dump_json())

        resp = self.http_client.http_delete(API_ACL_V1 + "/rules/macip", json=data)
        return resp

    def set_acl_allow_all(self) -> bool:
        for is_input in [True, False]:
            for role in [IfaceRoleTypes.LAN, IfaceRoleTypes.WAN]:
                rule = IpAclRule(
                    is_permit=AclAction.ACL_ACTION_API_PERMIT,
                    src_prefix=IPv4Network("0.0.0.0/0"),
                    dst_prefix=IPv4Network("0.0.0.0/0"),
                    proto=IpProtocol.IP_API_PROTO_HOPOPT,
                    src_port_first=0,
                    src_port_last=65535,
                    dst_port_first=0,
                    dst_port_last=65535,
                    tcp_flags_mask=0,
                    tcp_flags_value=0,
                    is_input=is_input,
                    priority=0,
                    interface_role=role,
                )
                resp = self.add_acl_rule(rule=rule)
                if not resp.status_code == HTTPStatus.OK:
                    return False
        return True

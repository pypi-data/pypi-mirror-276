# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: pyluba/proto/dev_net.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto


class WifiConfType(betterproto.Enum):
    DisconnectWifi = 0
    ForgetWifi = 1
    DirectConnectWifi = 2
    ReconnectWifi = 3
    set_enable = 4


class DrvUploadFileFileType(betterproto.Enum):
    FILE_TYPE_ALL = 0
    FILE_TYPE_SYSLOG = 1
    FILE_TYPE_NAVLOG = 2
    FILE_TYPE_RTKLOG = 3


class DrvDevInfoResult(betterproto.Enum):
    DRV_RESULT_FAIL = 0
    DRV_RESULT_SUC = 1
    DRV_RESULT_NOTSUP = 2


class SimCardSta(betterproto.Enum):
    SIM_NONE = 0
    SIM_NO_CARD = 1
    SIM_INVALID = 2
    SIM_INPUT_PIN = 3
    SIM_INPUT_PUK = 4
    SIM_OK = 5


class MnetLinkType(betterproto.Enum):
    MNET_LINK_NONE = 0
    MNET_LINK_2G = 1
    MNET_LINK_3G = 2
    MNET_LINK_4G = 3


class ApnAuthType(betterproto.Enum):
    APN_AUTH_NONE = 0
    APN_AUTH_PAP = 1
    APN_AUTH_CHAP = 2
    APN_AUTH_PAP_CHAP = 3


class NetType(betterproto.Enum):
    NET_TYPE_WIFI = 0
    NET_TYPE_MNET = 1


class IotConctrlType(betterproto.Enum):
    IOT_TYPE_OFFLINE = 0
    IOT_TYPE_ONLINE = 1
    IOT_TYPE_RESET = 2


@dataclass
class DrvWifiUpload(betterproto.Message):
    wifi_msg_upload: int = betterproto.int32_field(1)


@dataclass
class DrvWifiList(betterproto.Message):
    nvs_wifi_upload: int = betterproto.int32_field(1)


@dataclass
class DrvWifiSet(betterproto.Message):
    config_param: int = betterproto.int32_field(1)
    confssid: str = betterproto.string_field(2)
    wifi_enable: bool = betterproto.bool_field(3)


@dataclass
class DrvWifiMsg(betterproto.Message):
    status1: bool = betterproto.bool_field(1)
    status2: bool = betterproto.bool_field(2)
    ip: str = betterproto.string_field(3)
    msgssid: str = betterproto.string_field(4)
    password: str = betterproto.string_field(5)
    rssi: int = betterproto.int32_field(6)
    productkey: str = betterproto.string_field(7)
    devicename: str = betterproto.string_field(8)
    wifi_enable: bool = betterproto.bool_field(9)


@dataclass
class DrvWifiConf(betterproto.Message):
    succ_flag: bool = betterproto.bool_field(1)
    code: int = betterproto.int32_field(2)
    confssid: str = betterproto.string_field(3)


@dataclass
class DrvListUpload(betterproto.Message):
    sum: int = betterproto.int32_field(1)
    current: int = betterproto.int32_field(2)
    status: int = betterproto.int32_field(3)
    memssid: str = betterproto.string_field(4)
    rssi: int = betterproto.int32_field(5)


@dataclass
class DrvUploadFileReq(betterproto.Message):
    biz_id: str = betterproto.string_field(1)
    url: str = betterproto.string_field(2)
    user_id: str = betterproto.string_field(3)
    num: int = betterproto.int32_field(4)
    type: int = betterproto.int32_field(5)


@dataclass
class DrvUploadFileCancel(betterproto.Message):
    biz_id: str = betterproto.string_field(1)


@dataclass
class DrvUploadFileToAppReq(betterproto.Message):
    biz_id: str = betterproto.string_field(1)
    operation: int = betterproto.int32_field(2)
    server_ip: float = betterproto.fixed32_field(3)
    server_port: int = betterproto.int32_field(4)
    num: int = betterproto.int32_field(5)
    type: int = betterproto.int32_field(6)


@dataclass
class DrvUploadFileToAppRsp(betterproto.Message):
    biz_id: str = betterproto.string_field(1)
    operation: int = betterproto.int32_field(2)
    result: int = betterproto.int32_field(3)


@dataclass
class DrvDevInfoReqId(betterproto.Message):
    id: int = betterproto.int32_field(1)
    type: int = betterproto.int32_field(2)


@dataclass
class DrvDevInfoRespId(betterproto.Message):
    id: int = betterproto.int32_field(1)
    type: int = betterproto.int32_field(2)
    res: DrvDevInfoResult = betterproto.enum_field(3)
    info: str = betterproto.string_field(4)


@dataclass
class DrvDevInfoReq(betterproto.Message):
    req_ids: List["DrvDevInfoReqId"] = betterproto.message_field(1)


@dataclass
class DrvDevInfoResp(betterproto.Message):
    resp_ids: List["DrvDevInfoRespId"] = betterproto.message_field(1)


@dataclass
class DrvUpgradeReport(betterproto.Message):
    devname: str = betterproto.string_field(1)
    otaid: str = betterproto.string_field(2)
    version: str = betterproto.string_field(3)
    progress: int = betterproto.int32_field(4)
    result: int = betterproto.int32_field(5)
    message: str = betterproto.string_field(6)
    properties: str = betterproto.string_field(7)


@dataclass
class WifiIotStatusReport(betterproto.Message):
    wifi_connected: bool = betterproto.bool_field(1)
    iot_connected: bool = betterproto.bool_field(2)
    productkey: str = betterproto.string_field(3)
    devicename: str = betterproto.string_field(4)


@dataclass
class BleTestBytes(betterproto.Message):
    seqs: int = betterproto.int32_field(1)
    data: List[float] = betterproto.fixed32_field(2)


@dataclass
class GetNetworkInfoReq(betterproto.Message):
    req_ids: int = betterproto.int32_field(1)


@dataclass
class GetNetworkInfoRsp(betterproto.Message):
    req_ids: int = betterproto.int32_field(1)
    wifi_ssid: str = betterproto.string_field(2)
    wifi_mac: str = betterproto.string_field(3)
    wifi_rssi: int = betterproto.int32_field(4)
    ip: float = betterproto.fixed32_field(5)
    mask: float = betterproto.fixed32_field(6)
    gateway: float = betterproto.fixed32_field(7)


@dataclass
class MnetInetStatus(betterproto.Message):
    connect: bool = betterproto.bool_field(1)
    ip: float = betterproto.fixed32_field(2)
    mask: float = betterproto.fixed32_field(3)
    gateway: float = betterproto.fixed32_field(4)


@dataclass
class MnetInfo(betterproto.Message):
    model: str = betterproto.string_field(1)
    revision: str = betterproto.string_field(2)
    imei: str = betterproto.string_field(3)
    sim: "SimCardSta" = betterproto.enum_field(4)
    imsi: str = betterproto.string_field(5)
    link_type: "MnetLinkType" = betterproto.enum_field(6)
    rssi: int = betterproto.int32_field(7)
    inet: "MnetInetStatus" = betterproto.message_field(8)


@dataclass
class GetMnetInfoReq(betterproto.Message):
    req_ids: int = betterproto.int32_field(1)


@dataclass
class GetMnetInfoRsp(betterproto.Message):
    req_ids: int = betterproto.int32_field(1)
    result: int = betterproto.int32_field(2)
    mnet: MnetInfo = betterproto.message_field(3)


@dataclass
class MnetApn(betterproto.Message):
    cid: int = betterproto.int32_field(1)
    apn_alias: str = betterproto.string_field(2)
    apn_name: str = betterproto.string_field(3)
    auth: "ApnAuthType" = betterproto.enum_field(4)
    username: str = betterproto.string_field(5)
    password: str = betterproto.string_field(6)


@dataclass
class MnetApnCfg(betterproto.Message):
    apn_used_idx: int = betterproto.int32_field(1)
    apn: List["MnetApn"] = betterproto.message_field(2)


@dataclass
class MnetApnSetCfg(betterproto.Message):
    use_default: bool = betterproto.bool_field(1)
    cfg: "MnetApnCfg" = betterproto.message_field(2)


@dataclass
class MnetCfg(betterproto.Message):
    mnet_enable: bool = betterproto.bool_field(1)
    inet_enable: bool = betterproto.bool_field(2)
    type: "NetType" = betterproto.enum_field(3)
    apn: "MnetApnSetCfg" = betterproto.message_field(4)
    auto_select: bool = betterproto.bool_field(5)


@dataclass
class GetMnetCfgReq(betterproto.Message):
    req_ids: int = betterproto.int32_field(1)


@dataclass
class GetMnetCfgRsp(betterproto.Message):
    req_ids: int = betterproto.int32_field(1)
    result: int = betterproto.int32_field(2)
    cfg: "MnetCfg" = betterproto.message_field(3)


@dataclass
class SetMnetCfgReq(betterproto.Message):
    req_ids: int = betterproto.int32_field(1)
    cfg: "MnetCfg" = betterproto.message_field(2)


@dataclass
class SetMnetCfgRsp(betterproto.Message):
    req_ids: int = betterproto.int32_field(1)
    result: int = betterproto.int32_field(2)


@dataclass
class DrvDebugDdsZmq(betterproto.Message):
    is_enable: bool = betterproto.bool_field(1)
    rx_topic_name: str = betterproto.string_field(2)
    tx_zmq_url: str = betterproto.string_field(3)


@dataclass
class SetDrvBleMTU(betterproto.Message):
    mtu_count: int = betterproto.int32_field(1)


@dataclass
class DevNet(betterproto.Message):
    todev_ble_sync: int = betterproto.int32_field(1, group="NetSubType")
    todev__conf_type: "WifiConfType" = betterproto.enum_field(2, group="NetSubType")
    todev__wifi_msg_upload: "DrvWifiUpload" = betterproto.message_field(
        3, group="NetSubType"
    )
    todev__wifi_list_upload: "DrvWifiList" = betterproto.message_field(
        4, group="NetSubType"
    )
    todev__wifi__configuration: "DrvWifiSet" = betterproto.message_field(
        5, group="NetSubType"
    )
    toapp__wifi_msg: "DrvWifiMsg" = betterproto.message_field(6, group="NetSubType")
    toapp__wifi_conf: "DrvWifiConf" = betterproto.message_field(7, group="NetSubType")
    toapp__list_upload: "DrvListUpload" = betterproto.message_field(
        8, group="NetSubType"
    )
    todev_req_log_info: "DrvUploadFileReq" = betterproto.message_field(
        9, group="NetSubType"
    )
    todev_log_data_cancel: "DrvUploadFileCancel" = betterproto.message_field(
        10, group="NetSubType"
    )
    todev_devinfo_req: "DrvDevInfoReq" = betterproto.message_field(
        11, group="NetSubType"
    )
    toapp_devinfo_resp: "DrvDevInfoResp" = betterproto.message_field(
        12, group="NetSubType"
    )
    toapp_upgrade_report: "DrvUpgradeReport" = betterproto.message_field(
        13, group="NetSubType"
    )
    toapp_wifi_iot_status: "WifiIotStatusReport" = betterproto.message_field(
        14, group="NetSubType"
    )
    todev_uploadfile_req: "DrvUploadFileToAppReq" = betterproto.message_field(
        15, group="NetSubType"
    )
    toapp_uploadfile_rsp: "DrvUploadFileToAppRsp" = betterproto.message_field(
        16, group="NetSubType"
    )
    todev_networkinfo_req: "GetNetworkInfoReq" = betterproto.message_field(
        17, group="NetSubType"
    )
    toapp_networkinfo_rsp: "GetNetworkInfoRsp" = betterproto.message_field(
        18, group="NetSubType"
    )
    bir_testdata: "BleTestBytes" = betterproto.message_field(19, group="NetSubType")
    todev_mnet_info_req: "GetMnetInfoReq" = betterproto.message_field(
        20, group="NetSubType"
    )
    toapp_mnet_info_rsp: "GetMnetInfoRsp" = betterproto.message_field(
        21, group="NetSubType"
    )
    todev_get_mnet_cfg_req: "GetMnetCfgReq" = betterproto.message_field(
        22, group="NetSubType"
    )
    toapp_get_mnet_cfg_rsp: "GetMnetCfgRsp" = betterproto.message_field(
        23, group="NetSubType"
    )
    todev_set_mnet_cfg_req: "SetMnetCfgReq" = betterproto.message_field(
        24, group="NetSubType"
    )
    toapp_set_mnet_cfg_rsp: "SetMnetCfgRsp" = betterproto.message_field(
        25, group="NetSubType"
    )
    todev_set_dds2zmq: "DrvDebugDdsZmq" = betterproto.message_field(
        26, group="NetSubType"
    )
    todev_set_ble_mtu: "SetDrvBleMTU" = betterproto.message_field(
        27, group="NetSubType"
    )
    todev_set_iot_offline_req: "IotConctrlType" = betterproto.enum_field(
        28, group="NetSubType"
    )

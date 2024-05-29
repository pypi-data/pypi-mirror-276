# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pyluba/proto/dev_net.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1apyluba/proto/dev_net.proto\"(\n\rDrvWifiUpload\x12\x17\n\x0fWifi_Msg_Upload\x18\x01 \x01(\x05\"&\n\x0b\x44rvWifiList\x12\x17\n\x0fNVS_Wifi_Upload\x18\x01 \x01(\x05\"H\n\nDrvWifiSet\x12\x13\n\x0b\x63onfigParam\x18\x01 \x01(\x05\x12\x10\n\x08\x43onfssid\x18\x02 \x01(\t\x12\x13\n\x0bwifi_enable\x18\x03 \x01(\x08\"\xa8\x01\n\nDrvWifiMsg\x12\x0f\n\x07status1\x18\x01 \x01(\x08\x12\x0f\n\x07status2\x18\x02 \x01(\x08\x12\n\n\x02IP\x18\x03 \x01(\t\x12\x0f\n\x07Msgssid\x18\x04 \x01(\t\x12\x10\n\x08password\x18\x05 \x01(\t\x12\x0c\n\x04rssi\x18\x06 \x01(\x05\x12\x12\n\nproductkey\x18\x07 \x01(\t\x12\x12\n\ndevicename\x18\x08 \x01(\t\x12\x13\n\x0bwifi_enable\x18\t \x01(\x08\"?\n\x0b\x44rvWifiConf\x12\x10\n\x08succFlag\x18\x01 \x01(\x08\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x05\x12\x10\n\x08\x43onfssid\x18\x03 \x01(\t\"\\\n\rDrvListUpload\x12\x0b\n\x03sum\x18\x01 \x01(\x05\x12\x0f\n\x07\x63urrent\x18\x02 \x01(\x05\x12\x0e\n\x06status\x18\x03 \x01(\x05\x12\x0f\n\x07Memssid\x18\x04 \x01(\t\x12\x0c\n\x04rssi\x18\x05 \x01(\x05\"Y\n\x10\x44rvUploadFileReq\x12\r\n\x05\x62izId\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\t\x12\x0e\n\x06userId\x18\x03 \x01(\t\x12\x0b\n\x03num\x18\x04 \x01(\x05\x12\x0c\n\x04type\x18\x05 \x01(\x05\"$\n\x13\x44rvUploadFileCancel\x12\r\n\x05\x62izId\x18\x01 \x01(\t\"z\n\x15\x44rvUploadFileToAppReq\x12\r\n\x05\x62izId\x18\x01 \x01(\t\x12\x11\n\toperation\x18\x02 \x01(\x05\x12\x10\n\x08serverIp\x18\x03 \x01(\x07\x12\x12\n\nserverPort\x18\x04 \x01(\x05\x12\x0b\n\x03num\x18\x05 \x01(\x05\x12\x0c\n\x04type\x18\x06 \x01(\x05\"I\n\x15\x44rvUploadFileToAppRsp\x12\r\n\x05\x62izId\x18\x01 \x01(\t\x12\x11\n\toperation\x18\x02 \x01(\x05\x12\x0e\n\x06result\x18\x03 \x01(\x05\"+\n\x0f\x44rvDevInfoReqId\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04type\x18\x02 \x01(\x05\"Z\n\x10\x44rvDevInfoRespId\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04type\x18\x02 \x01(\x05\x12\x1e\n\x03res\x18\x03 \x01(\x0e\x32\x11.DrvDevInfoResult\x12\x0c\n\x04info\x18\x04 \x01(\t\"2\n\rDrvDevInfoReq\x12!\n\x07req_ids\x18\x01 \x03(\x0b\x32\x10.DrvDevInfoReqId\"5\n\x0e\x44rvDevInfoResp\x12#\n\x08resp_ids\x18\x01 \x03(\x0b\x32\x11.DrvDevInfoRespId\"\x8a\x01\n\x10\x44rvUpgradeReport\x12\x0f\n\x07\x64\x65vname\x18\x01 \x01(\t\x12\r\n\x05otaid\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x10\n\x08progress\x18\x04 \x01(\x05\x12\x0e\n\x06result\x18\x05 \x01(\x05\x12\x0f\n\x07message\x18\x06 \x01(\t\x12\x12\n\nproperties\x18\x07 \x01(\t\"l\n\x13WifiIotStatusReport\x12\x16\n\x0ewifi_connected\x18\x01 \x01(\x08\x12\x15\n\riot_connected\x18\x02 \x01(\x08\x12\x12\n\nproductkey\x18\x03 \x01(\t\x12\x12\n\ndevicename\x18\x04 \x01(\t\"*\n\x0c\x42leTestBytes\x12\x0c\n\x04seqs\x18\x01 \x01(\x05\x12\x0c\n\x04\x64\x61ta\x18\x02 \x03(\x07\"$\n\x11GetNetworkInfoReq\x12\x0f\n\x07req_ids\x18\x01 \x01(\x05\"\x87\x01\n\x11GetNetworkInfoRsp\x12\x0f\n\x07req_ids\x18\x01 \x01(\x05\x12\x11\n\twifi_ssid\x18\x02 \x01(\t\x12\x10\n\x08wifi_mac\x18\x03 \x01(\t\x12\x11\n\twifi_rssi\x18\x04 \x01(\x05\x12\n\n\x02ip\x18\x05 \x01(\x07\x12\x0c\n\x04mask\x18\x06 \x01(\x07\x12\x0f\n\x07gateway\x18\x07 \x01(\x07\"N\n\x10mnet_inet_status\x12\x0f\n\x07\x63onnect\x18\x01 \x01(\x08\x12\n\n\x02ip\x18\x02 \x01(\x07\x12\x0c\n\x04mask\x18\x03 \x01(\x07\x12\x0f\n\x07gateway\x18\x04 \x01(\x07\"\xb6\x01\n\x08MnetInfo\x12\r\n\x05model\x18\x01 \x01(\t\x12\x10\n\x08revision\x18\x02 \x01(\t\x12\x0c\n\x04imei\x18\x03 \x01(\t\x12\x1a\n\x03sim\x18\x04 \x01(\x0e\x32\r.sim_card_sta\x12\x0c\n\x04imsi\x18\x05 \x01(\t\x12\"\n\tlink_type\x18\x06 \x01(\x0e\x32\x0f.mnet_link_type\x12\x0c\n\x04rssi\x18\x07 \x01(\x05\x12\x1f\n\x04inet\x18\x08 \x01(\x0b\x32\x11.mnet_inet_status\"!\n\x0eGetMnetInfoReq\x12\x0f\n\x07req_ids\x18\x01 \x01(\x05\"J\n\x0eGetMnetInfoRsp\x12\x0f\n\x07req_ids\x18\x01 \x01(\x05\x12\x0e\n\x06result\x18\x02 \x01(\x05\x12\x17\n\x04mnet\x18\x03 \x01(\x0b\x32\t.MnetInfo\"}\n\x07MnetApn\x12\x0b\n\x03\x63id\x18\x01 \x01(\x05\x12\x11\n\tapn_alias\x18\x02 \x01(\t\x12\x10\n\x08\x61pn_name\x18\x03 \x01(\t\x12\x1c\n\x04\x61uth\x18\x04 \x01(\x0e\x32\x0e.apn_auth_type\x12\x10\n\x08username\x18\x05 \x01(\t\x12\x10\n\x08password\x18\x06 \x01(\t\"9\n\nMnetApnCfg\x12\x14\n\x0c\x61pn_used_idx\x18\x01 \x01(\x05\x12\x15\n\x03\x61pn\x18\x02 \x03(\x0b\x32\x08.MnetApn\">\n\rMnetApnSetCfg\x12\x13\n\x0buse_default\x18\x01 \x01(\x08\x12\x18\n\x03\x63\x66g\x18\x02 \x01(\x0b\x32\x0b.MnetApnCfg\"~\n\x07MnetCfg\x12\x13\n\x0bmnet_enable\x18\x01 \x01(\x08\x12\x13\n\x0binet_enable\x18\x02 \x01(\x08\x12\x17\n\x04type\x18\x03 \x01(\x0e\x32\t.net_type\x12\x1b\n\x03\x61pn\x18\x04 \x01(\x0b\x32\x0e.MnetApnSetCfg\x12\x13\n\x0b\x61uto_select\x18\x05 \x01(\x08\" \n\rGetMnetCfgReq\x12\x0f\n\x07req_ids\x18\x01 \x01(\x05\"G\n\rGetMnetCfgRsp\x12\x0f\n\x07req_ids\x18\x01 \x01(\x05\x12\x0e\n\x06result\x18\x02 \x01(\x05\x12\x15\n\x03\x63\x66g\x18\x03 \x01(\x0b\x32\x08.MnetCfg\"7\n\rSetMnetCfgReq\x12\x0f\n\x07req_ids\x18\x01 \x01(\x05\x12\x15\n\x03\x63\x66g\x18\x02 \x01(\x0b\x32\x08.MnetCfg\"0\n\rSetMnetCfgRsp\x12\x0f\n\x07req_ids\x18\x01 \x01(\x05\x12\x0e\n\x06result\x18\x02 \x01(\x05\"N\n\x0e\x44rvDebugDdsZmq\x12\x11\n\tis_enable\x18\x01 \x01(\x08\x12\x15\n\rrx_topic_name\x18\x02 \x01(\t\x12\x12\n\ntx_zmq_url\x18\x03 \x01(\t\"!\n\x0cSetDrvBleMTU\x12\x11\n\tmtu_count\x18\x01 \x01(\x05\"\xca\n\n\x06\x44\x65vNet\x12\x18\n\x0etodev_ble_sync\x18\x01 \x01(\x05H\x00\x12\'\n\x0etodev_ConfType\x18\x02 \x01(\x0e\x32\r.WifiConfTypeH\x00\x12-\n\x13todev_WifiMsgUpload\x18\x03 \x01(\x0b\x32\x0e.DrvWifiUploadH\x00\x12,\n\x14todev_WifiListUpload\x18\x04 \x01(\x0b\x32\x0c.DrvWifiListH\x00\x12/\n\x18todev_Wifi_Configuration\x18\x05 \x01(\x0b\x32\x0b.DrvWifiSetH\x00\x12$\n\rtoapp_WifiMsg\x18\x06 \x01(\x0b\x32\x0b.DrvWifiMsgH\x00\x12&\n\x0etoapp_WifiConf\x18\x07 \x01(\x0b\x32\x0c.DrvWifiConfH\x00\x12*\n\x10toapp_ListUpload\x18\x08 \x01(\x0b\x32\x0e.DrvListUploadH\x00\x12/\n\x12todev_req_log_info\x18\t \x01(\x0b\x32\x11.DrvUploadFileReqH\x00\x12\x35\n\x15todev_log_data_cancel\x18\n \x01(\x0b\x32\x14.DrvUploadFileCancelH\x00\x12+\n\x11todev_devinfo_req\x18\x0b \x01(\x0b\x32\x0e.DrvDevInfoReqH\x00\x12-\n\x12toapp_devinfo_resp\x18\x0c \x01(\x0b\x32\x0f.DrvDevInfoRespH\x00\x12\x31\n\x14toapp_upgrade_report\x18\r \x01(\x0b\x32\x11.DrvUpgradeReportH\x00\x12\x35\n\x15toapp_wifi_iot_status\x18\x0e \x01(\x0b\x32\x14.WifiIotStatusReportH\x00\x12\x36\n\x14todev_uploadfile_req\x18\x0f \x01(\x0b\x32\x16.DrvUploadFileToAppReqH\x00\x12\x36\n\x14toapp_uploadfile_rsp\x18\x10 \x01(\x0b\x32\x16.DrvUploadFileToAppRspH\x00\x12\x33\n\x15todev_networkinfo_req\x18\x11 \x01(\x0b\x32\x12.GetNetworkInfoReqH\x00\x12\x33\n\x15toapp_networkinfo_rsp\x18\x12 \x01(\x0b\x32\x12.GetNetworkInfoRspH\x00\x12%\n\x0c\x62ir_testdata\x18\x13 \x01(\x0b\x32\r.BleTestBytesH\x00\x12.\n\x13todev_mnet_info_req\x18\x14 \x01(\x0b\x32\x0f.GetMnetInfoReqH\x00\x12.\n\x13toapp_mnet_info_rsp\x18\x15 \x01(\x0b\x32\x0f.GetMnetInfoRspH\x00\x12\x30\n\x16todev_get_mnet_cfg_req\x18\x16 \x01(\x0b\x32\x0e.GetMnetCfgReqH\x00\x12\x30\n\x16toapp_get_mnet_cfg_rsp\x18\x17 \x01(\x0b\x32\x0e.GetMnetCfgRspH\x00\x12\x30\n\x16todev_set_mnet_cfg_req\x18\x18 \x01(\x0b\x32\x0e.SetMnetCfgReqH\x00\x12\x30\n\x16toapp_set_mnet_cfg_rsp\x18\x19 \x01(\x0b\x32\x0e.SetMnetCfgRspH\x00\x12,\n\x11todev_set_dds2zmq\x18\x1a \x01(\x0b\x32\x0f.DrvDebugDdsZmqH\x00\x12*\n\x11todev_set_ble_mtu\x18\x1b \x01(\x0b\x32\r.SetDrvBleMTUH\x00\x12\x36\n\x19todev_set_iot_offline_req\x18\x1c \x01(\x0e\x32\x11.iot_conctrl_typeH\x00\x42\x0c\n\nNetSubType*l\n\x0cWifiConfType\x12\x12\n\x0e\x44isconnectWifi\x10\x00\x12\x0e\n\nForgetWifi\x10\x01\x12\x15\n\x11\x44irectConnectWifi\x10\x02\x12\x11\n\rReconnectWifi\x10\x03\x12\x0e\n\nset_enable\x10\x04*l\n\x15\x44rvUploadFileFileType\x12\x11\n\rFILE_TYPE_ALL\x10\x00\x12\x14\n\x10\x46ILE_TYPE_SYSLOG\x10\x01\x12\x14\n\x10\x46ILE_TYPE_NAVLOG\x10\x02\x12\x14\n\x10\x46ILE_TYPE_RTKLOG\x10\x03*R\n\x10\x44rvDevInfoResult\x12\x13\n\x0f\x44RV_RESULT_FAIL\x10\x00\x12\x12\n\x0e\x44RV_RESULT_SUC\x10\x01\x12\x15\n\x11\x44RV_RESULT_NOTSUP\x10\x02*p\n\x0csim_card_sta\x12\x0c\n\x08SIM_NONE\x10\x00\x12\x0f\n\x0bSIM_NO_CARD\x10\x01\x12\x0f\n\x0bSIM_INVALID\x10\x02\x12\x11\n\rSIM_INPUT_PIN\x10\x03\x12\x11\n\rSIM_INPUT_PUK\x10\x04\x12\n\n\x06SIM_OK\x10\x05*Z\n\x0emnet_link_type\x12\x12\n\x0eMNET_LINK_NONE\x10\x00\x12\x10\n\x0cMNET_LINK_2G\x10\x01\x12\x10\n\x0cMNET_LINK_3G\x10\x02\x12\x10\n\x0cMNET_LINK_4G\x10\x03*^\n\rapn_auth_type\x12\x11\n\rAPN_AUTH_NONE\x10\x00\x12\x10\n\x0c\x41PN_AUTH_PAP\x10\x01\x12\x11\n\rAPN_AUTH_CHAP\x10\x02\x12\x15\n\x11\x41PN_AUTH_PAP_CHAP\x10\x03*0\n\x08net_type\x12\x11\n\rNET_TYPE_WIFI\x10\x00\x12\x11\n\rNET_TYPE_MNET\x10\x01*Q\n\x10iot_conctrl_type\x12\x14\n\x10IOT_TYPE_OFFLINE\x10\x00\x12\x13\n\x0fIOT_TYPE_ONLINE\x10\x01\x12\x12\n\x0eIOT_TYPE_RESET\x10\x02\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'pyluba.proto.dev_net_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _WIFICONFTYPE._serialized_start=3999
  _WIFICONFTYPE._serialized_end=4107
  _DRVUPLOADFILEFILETYPE._serialized_start=4109
  _DRVUPLOADFILEFILETYPE._serialized_end=4217
  _DRVDEVINFORESULT._serialized_start=4219
  _DRVDEVINFORESULT._serialized_end=4301
  _SIM_CARD_STA._serialized_start=4303
  _SIM_CARD_STA._serialized_end=4415
  _MNET_LINK_TYPE._serialized_start=4417
  _MNET_LINK_TYPE._serialized_end=4507
  _APN_AUTH_TYPE._serialized_start=4509
  _APN_AUTH_TYPE._serialized_end=4603
  _NET_TYPE._serialized_start=4605
  _NET_TYPE._serialized_end=4653
  _IOT_CONCTRL_TYPE._serialized_start=4655
  _IOT_CONCTRL_TYPE._serialized_end=4736
  _DRVWIFIUPLOAD._serialized_start=30
  _DRVWIFIUPLOAD._serialized_end=70
  _DRVWIFILIST._serialized_start=72
  _DRVWIFILIST._serialized_end=110
  _DRVWIFISET._serialized_start=112
  _DRVWIFISET._serialized_end=184
  _DRVWIFIMSG._serialized_start=187
  _DRVWIFIMSG._serialized_end=355
  _DRVWIFICONF._serialized_start=357
  _DRVWIFICONF._serialized_end=420
  _DRVLISTUPLOAD._serialized_start=422
  _DRVLISTUPLOAD._serialized_end=514
  _DRVUPLOADFILEREQ._serialized_start=516
  _DRVUPLOADFILEREQ._serialized_end=605
  _DRVUPLOADFILECANCEL._serialized_start=607
  _DRVUPLOADFILECANCEL._serialized_end=643
  _DRVUPLOADFILETOAPPREQ._serialized_start=645
  _DRVUPLOADFILETOAPPREQ._serialized_end=767
  _DRVUPLOADFILETOAPPRSP._serialized_start=769
  _DRVUPLOADFILETOAPPRSP._serialized_end=842
  _DRVDEVINFOREQID._serialized_start=844
  _DRVDEVINFOREQID._serialized_end=887
  _DRVDEVINFORESPID._serialized_start=889
  _DRVDEVINFORESPID._serialized_end=979
  _DRVDEVINFOREQ._serialized_start=981
  _DRVDEVINFOREQ._serialized_end=1031
  _DRVDEVINFORESP._serialized_start=1033
  _DRVDEVINFORESP._serialized_end=1086
  _DRVUPGRADEREPORT._serialized_start=1089
  _DRVUPGRADEREPORT._serialized_end=1227
  _WIFIIOTSTATUSREPORT._serialized_start=1229
  _WIFIIOTSTATUSREPORT._serialized_end=1337
  _BLETESTBYTES._serialized_start=1339
  _BLETESTBYTES._serialized_end=1381
  _GETNETWORKINFOREQ._serialized_start=1383
  _GETNETWORKINFOREQ._serialized_end=1419
  _GETNETWORKINFORSP._serialized_start=1422
  _GETNETWORKINFORSP._serialized_end=1557
  _MNET_INET_STATUS._serialized_start=1559
  _MNET_INET_STATUS._serialized_end=1637
  _MNETINFO._serialized_start=1640
  _MNETINFO._serialized_end=1822
  _GETMNETINFOREQ._serialized_start=1824
  _GETMNETINFOREQ._serialized_end=1857
  _GETMNETINFORSP._serialized_start=1859
  _GETMNETINFORSP._serialized_end=1933
  _MNETAPN._serialized_start=1935
  _MNETAPN._serialized_end=2060
  _MNETAPNCFG._serialized_start=2062
  _MNETAPNCFG._serialized_end=2119
  _MNETAPNSETCFG._serialized_start=2121
  _MNETAPNSETCFG._serialized_end=2183
  _MNETCFG._serialized_start=2185
  _MNETCFG._serialized_end=2311
  _GETMNETCFGREQ._serialized_start=2313
  _GETMNETCFGREQ._serialized_end=2345
  _GETMNETCFGRSP._serialized_start=2347
  _GETMNETCFGRSP._serialized_end=2418
  _SETMNETCFGREQ._serialized_start=2420
  _SETMNETCFGREQ._serialized_end=2475
  _SETMNETCFGRSP._serialized_start=2477
  _SETMNETCFGRSP._serialized_end=2525
  _DRVDEBUGDDSZMQ._serialized_start=2527
  _DRVDEBUGDDSZMQ._serialized_end=2605
  _SETDRVBLEMTU._serialized_start=2607
  _SETDRVBLEMTU._serialized_end=2640
  _DEVNET._serialized_start=2643
  _DEVNET._serialized_end=3997
# @@protoc_insertion_point(module_scope)

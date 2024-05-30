from pyluba.proto import luba_msg_pb2, dev_net_pb2, mctrl_sys_pb2
from pyluba.proto.mctrl_sys import RptInfoType


class LubaCommandProtoMQTT:
    """MQTT commands for Luba."""

    async def send_order_msg_net(self, build) -> bytes:
        luba_msg = luba_msg_pb2.LubaMsg(
            msgtype=luba_msg_pb2.MsgCmdType.MSG_CMD_TYPE_ESP,
            sender=luba_msg_pb2.MsgDevice.DEV_MOBILEAPP,
            rcver=luba_msg_pb2.MsgDevice.DEV_COMM_ESP,
            msgattr=luba_msg_pb2.MsgAttr.MSG_ATTR_REQ,
            seqs=1,
            version=1,
            subtype=1,
            net=build)

        return luba_msg.SerializeToString()


    async def start_work_job(self):
        luba_msg = luba_msg_pb2.LubaMsg(
            msgtype=luba_msg_pb2.MsgCmdType.MSG_CMD_TYPE_NAV,
            sender=luba_msg_pb2.MsgDevice.DEV_MOBILEAPP,
            rcver=luba_msg_pb2.MsgDevice.DEV_MAINCTL,
            msgattr=luba_msg_pb2.MsgAttr.MSG_ATTR_REQ,
            seqs=1,
            version=1,
            subtype=1,
            nav=mctrl_nav_pb2.MctlNav(
                todev_taskctrl=mctrl_nav_pb2.NavTaskCtrl(
                    type=1,
                    action=1,
                    result=0
                )
            )
        )
        return luba_msg.SerializeToString()

    def pause_execute_task(self):
        luba_msg = luba_msg_pb2.LubaMsg(
            msgtype=luba_msg_pb2.MsgCmdType.MSG_CMD_TYPE_NAV,
            sender=luba_msg_pb2.MsgDevice.DEV_MOBILEAPP,
            rcver=luba_msg_pb2.MsgDevice.DEV_MAINCTL,
            msgattr=luba_msg_pb2.MsgAttr.MSG_ATTR_REQ,
            seqs=1,
            version=1,
            subtype=1,
            nav=mctrl_nav_pb2.MctlNav(
                todev_taskctrl=mctrl_nav_pb2.NavTaskCtrl(
                    type=1,
                    action=2,
                    result=0
                )
            )
        )

        return luba_msg.SerializeToString()

    async def return_to_dock(self):
        mctrlNav = mctrl_nav_pb2.MctlNav()
        navTaskCtrl = mctrl_nav_pb2.NavTaskCtrl()
        navTaskCtrl.type = 1
        navTaskCtrl.action = 5
        navTaskCtrl.result = 0
        mctrlNav.todev_taskctrl.CopyFrom(navTaskCtrl)

        lubaMsg = luba_msg_pb2.LubaMsg()
        lubaMsg.msgtype = luba_msg_pb2.MsgCmdType.MSG_CMD_TYPE_NAV
        lubaMsg.sender = luba_msg_pb2.MsgDevice.DEV_MOBILEAPP
        lubaMsg.rcver = luba_msg_pb2.MsgDevice.DEV_MAINCTL
        lubaMsg.msgattr = luba_msg_pb2.MsgAttr.MSG_ATTR_REQ
        lubaMsg.seqs = 1
        lubaMsg.version = 1
        lubaMsg.subtype = 1
        lubaMsg.nav.CopyFrom(mctrlNav)
        return lubaMsg.SerializeToString()

    def get_report_cfg(self, timeout: int = 10000, period: int = 1000, no_change_period: int = 2000):
        mctlsys = mctrl_sys_pb2.MctlSys(
            todev_report_cfg=mctrl_sys_pb2.report_info_cfg(
                timeout=timeout,
                period=period,
                no_change_period=no_change_period,
                count=1
            )
        )

        mctlsys.todev_report_cfg.sub.append(
            RptInfoType.RIT_CONNECT.value
        )
        mctlsys.todev_report_cfg.sub.append(
            RptInfoType.RIT_RTK.value
        )
        mctlsys.todev_report_cfg.sub.append(
            RptInfoType.RIT_DEV_LOCAL.value
        )
        mctlsys.todev_report_cfg.sub.append(
            RptInfoType.RIT_WORK.value
        )
        mctlsys.todev_report_cfg.sub.append(
            RptInfoType.RIT_DEV_STA.value
        )
        mctlsys.todev_report_cfg.sub.append(
            RptInfoType.RIT_VISION_POINT.value
        )
        mctlsys.todev_report_cfg.sub.append(
            RptInfoType.RIT_VIO.value
        )
        mctlsys.todev_report_cfg.sub.append(
            RptInfoType.RIT_VISION_STATISTIC.value
        )

        lubaMsg = luba_msg_pb2.LubaMsg()
        lubaMsg.msgtype = luba_msg_pb2.MSG_CMD_TYPE_EMBED_SYS
        lubaMsg.sender = luba_msg_pb2.DEV_MOBILEAPP
        lubaMsg.rcver = luba_msg_pb2.DEV_MAINCTL
        lubaMsg.msgattr = luba_msg_pb2.MSG_ATTR_REQ
        lubaMsg.seqs = 1
        lubaMsg.version = 1
        lubaMsg.subtype = 1
        lubaMsg.sys.CopyFrom(mctlsys)
        return lubaMsg.SerializeToString()


"""BLE inherits MQTT because BLE has BLE only commands."""


class LubaCommandProtoBLE(LubaCommandProtoMQTT):
    """BLE commands for Luba."""

    def send_todev_ble_sync(self, sync_type: int) -> bytes:
        commEsp = dev_net_pb2.DevNet(
            todev_ble_sync=sync_type
        )

        lubaMsg = luba_msg_pb2.LubaMsg()
        lubaMsg.msgtype = luba_msg_pb2.MSG_CMD_TYPE_ESP
        lubaMsg.sender = luba_msg_pb2.DEV_MOBILEAPP
        lubaMsg.msgattr = luba_msg_pb2.MSG_ATTR_REQ
        lubaMsg.seqs = 1
        lubaMsg.version = 1
        lubaMsg.subtype = 1
        lubaMsg.net.CopyFrom(commEsp)
        return lubaMsg.SerializeToString()

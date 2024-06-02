from abc import ABC, abstractmethod
from websocket import create_connection
import websocket
import time
import _thread
import flatbuffers
from ubicoders_vrobots.vrobots_msgs.python.srv_omr_walls_generated import (
    SrvOMRWall,
    SrvOMRWallT,
)
from ..vrobots_msgs.python.states_generated import StatesMsgT
from ..vrobots_msgs.python.commands_generated import CommandMsgT
from ..vrobots_msgs.python.VROBOTS_CMDS import CMD_DICT
from .msg_helper import VRobotState


def ws_req_service(msg_packer, checker):
    ws = create_connection("ws://localhost:12740")

    keepRunning = True
    result = None
    while keepRunning:
        print("sending...")
        req_msg = msg_packer()
        ws.send(req_msg, opcode=0x2)
        rec_msg = ws.recv()
        keepRunning = checker(rec_msg)
        result = rec_msg
        time.sleep(1)
    print("Received '%s'" % result)
    ws.close()
    return result


def omrover_download_map():
    def msg_check(rec_msg):
        if rec_msg is None:
            return True
        if SrvOMRWall.SrvOMRWallBufferHasIdentifier(rec_msg, 0) is True:
            print("Received")
            return False
        else:
            return True

    def msg_packer():
        srv_omr_wall = SrvOMRWallT()
        srv_omr_wall.timestamp = time.time() * 1000.0
        srv_omr_wall.name = "python"
        srv_omr_wall.id = 0
        srv_omr_wall.reqSrcId = 2
        builder = flatbuffers.Builder(512)
        os = srv_omr_wall.Pack(builder)
        builder.Finish(os, b"SRV0")
        req_msg = builder.Output()
        return req_msg

    rec_msg = ws_req_service(msg_packer, msg_check)

    aa = SrvOMRWall.SrvOMRWallBufferHasIdentifier(rec_msg, 0)
    print(aa)

    objdata = SrvOMRWallT.InitFromPackedBuf(rec_msg, 0)
    name = objdata.name.decode("utf-8")
    omrover_map = objdata.vec3List
    print(f"Received {name}")
    for i, vec3 in enumerate(omrover_map):
        print(f"vec3[{i}]: {vec3.x}, {vec3.y}, {vec3.z}")


if __name__ == "__main__":
    omrover_download_map()

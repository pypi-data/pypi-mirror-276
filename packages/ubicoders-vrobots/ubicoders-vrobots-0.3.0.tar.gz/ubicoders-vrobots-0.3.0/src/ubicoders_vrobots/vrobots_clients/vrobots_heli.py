import flatbuffers
from ubicoders_vrobots.vrobots_msgs.python.VROBOTS_CMDS import CMD_DICT
from .msg_helper import VRobotState
from ..vrobots_msgs.python.states_generated import *
from ..vrobots_msgs.python.commands_generated import *
from .clientutils import VirtualRobot, System
import time


class Helicopter2D(VirtualRobot):
    def __init__(self) -> None:
        self.states: VRobotState = VRobotState(None)
        self.force: float = 0

    def pack_cmd_force(self) -> bytes:
        builder = flatbuffers.Builder(512)
        cmdMsgT = CommandMsgT()
        cmdMsgT.timestamp = time.time()
        cmdMsgT.name = "python"
        cmdMsgT.id = CMD_DICT["set_force"]
        cmdMsgT.float_val = self.force
        os = cmdMsgT.Pack(builder=builder)
        builder.Finish(os, b"CMD0")
        return builder.Output()

    def pack_setup(self) -> List[bytes]:
        ba_reset = self.pack_cmd_reset()
        return [ba_reset]

    def pack(self) -> List[bytes]:
        cmd_force = self.pack_cmd_force()
        return [cmd_force]


# ===============================================================================
# dev code
# ===============================================================================

heli = Helicopter2D()


class UbicodersMain:
    def __init__(self) -> None:
        pass

    def setup(self):
        # mr.mass = 2 kg
        pass

    def loop(self):
        states = heli.states
        # print(states.lin_pos)
        # print(states.lin_vel)

        heli.force = 20


if __name__ == "__main__":
    sys = System(heli, UbicodersMain())
    sys.start()

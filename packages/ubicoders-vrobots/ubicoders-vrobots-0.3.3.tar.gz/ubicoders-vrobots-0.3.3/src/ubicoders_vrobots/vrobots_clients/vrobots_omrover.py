import time
from .msg_helper import VRobotState
from ..vrobots_msgs.python.states_generated import *
from ..vrobots_msgs.python.commands_generated import *
from .clientutils import VirtualRobot, System
from ..vrobots_msgs.python.VROBOTS_CMDS import CMD_DICT


class OMRover(VirtualRobot):
    def __init__(self) -> None:
        super().__init__()
        self.states: VRobotState = VRobotState(None)
        self.actuators: List[float] = [0, 0, 0, 0]

    def pack_cmd_actuators(self) -> bytes:
        self.cmdMsgT = CommandMsgT()
        self.cmdMsgT.timestamp = time.time()
        self.cmdMsgT.name = "python"
        self.cmdMsgT.id = CMD_DICT["set_actuators"]
        self.cmdMsgT.floatArr = self.actuators
        return self.Tobj2bytes(self.cmdMsgT)

    def pack_setup(self) -> List[bytes]:
        ba_reset = self.pack_cmd_reset()
        self.setup_msg_list.append(ba_reset)

    def pack(self) -> List[bytes]:
        ba = self.pack_cmd_actuators()
        return [ba]


# ===============================================================================
# dev code
# ===============================================================================

omr = OMRover()


class UbicodersMain:
    def __init__(self) -> None:
        pass

    def setup(self):
        pass

    def loop(self):
        states = omr.states
        print(states)

        omr.actuators = [0, 0, 10, 20]


if __name__ == "__main__":
    sys = System(omr, UbicodersMain())
    sys.start()

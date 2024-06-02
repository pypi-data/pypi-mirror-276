import flatbuffers
from ubicoders_vrobots.vrobots_msgs.python.VROBOTS_CMDS import CMD_DICT
from .msg_helper import VRobotState
from ..vrobots_msgs.python.states_generated import *
from ..vrobots_msgs.python.commands_generated import *
from .clientutils import VirtualRobot, System


class Multirotor(VirtualRobot):
    def __init__(self) -> None:
        self.states = VRobotState(None)
        self.pwm = [900, 900, 900, 900]

    def set_pwm(self, m0, m1, m2, m3):
        self.pwm = [m0, m1, m2, m3]

    def pack_cmd_pwm(self) -> bytes:
        builder = flatbuffers.Builder(512)
        cmd_msg = CommandMsgT()
        cmd_msg.name = "python"
        cmd_msg.id = CMD_DICT["set_pwm"]
        cmd_msg.intArr = [int(num) for num in self.pwm]
        os = cmd_msg.Pack(builder)
        builder.Finish(os, b"CMD0")
        return builder.Output()

    def pack_setup(self) -> List[bytes]:
        cmd_reset = self.pack_cmd_reset()
        return [cmd_reset]

    def pack(self) -> List[bytes]:
        cmd_pwm = self.pack_cmd_pwm()
        return [cmd_pwm]


# ===============================================================================
# dev code
# ===============================================================================

mr = Multirotor()


class UbicodersMain:
    def __init__(self) -> None:
        pass

    def setup(self):
        # mr.mass = 2 kg
        pass

    def loop(self):
        states = mr.states
        print(states.accelerometer)
        print(states.gyroscope)
        print(states.euler)
        print(states.pwm)

        mr.set_pwm(m0=1500, m1=1500, m2=1500, m3=1500)


if __name__ == "__main__":
    sys = System(mr, UbicodersMain())
    sys.start()

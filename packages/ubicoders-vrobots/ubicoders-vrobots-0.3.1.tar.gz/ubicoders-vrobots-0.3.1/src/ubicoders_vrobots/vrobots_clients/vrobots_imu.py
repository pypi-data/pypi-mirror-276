import time
import numpy as np
from ubicoders_vrobots.vrobots_msgs.python.srv_imu_replay_generated import (
    SrvReplayMsgT,
    Vec3MsgT,
    Vec4MsgT,
)
from .msg_helper import VRobotState
from ..vrobots_msgs.python.states_generated import *
from ..vrobots_msgs.python.commands_generated import *
from .clientutils import VirtualRobot, System


class InertialSensor(VirtualRobot):
    def __init__(self) -> None:
        self.states = VRobotState(None)
        self.replayMsgT: SrvReplayMsgT = SrvReplayMsgT()
        self.replayMsgT.eulerGt = []
        self.replayMsgT.eulerEst = []

    def register_euler_gt_est(self, gt, est):
        """
        gt: (Nx3) numpy array
        est: (Nx3) numpy array
        """
        for i in range(gt.shape[0]):
            vec3gt = Vec3MsgT()
            vec3gt.x = gt[i, 0]
            vec3gt.y = gt[i, 1]
            vec3gt.z = gt[i, 2]
            vec3est = Vec3MsgT()
            vec3est.x = est[i, 0]
            vec3est.y = est[i, 1]
            vec3est.z = est[i, 2]
            self.replayMsgT.eulerGt.append(vec3gt)
            self.replayMsgT.eulerEst.append(vec3est)

    def pack_setup(self) -> List[bytes]:
        cmd_reset = self.pack_cmd_reset()
        replay_msg = self.Tobj2bytes(self.replayMsgT)
        return [cmd_reset, replay_msg]

    def pack(self) -> List[bytes]:
        self.replayMsgT.timestamp = time.time()
        ba = self.Tobj2bytes(self.replayMsgT)
        return [ba]


# ===============================================================================
# dev code
# ===============================================================================

imu = InertialSensor()


class UbicodersMain:
    def __init__(self) -> None:
        pass

    def setup(self):
        gt = np.zeros((10, 3))
        est = np.zeros((10, 3))
        imu.register_euler_gt_est(gt, est)

    def loop(self):
        states = imu.states
        # print(states.accelerometer)
        # print(states.gyroscope)
        # print(states.euler)


if __name__ == "__main__":
    sys = System(imu, UbicodersMain(), duration=1)
    sys.start()

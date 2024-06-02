from abc import ABC, abstractmethod
import websocket
import time
import _thread
import flatbuffers
from ..vrobots_msgs.python.states_generated import StatesMsgT
from ..vrobots_msgs.python.commands_generated import CommandMsgT
from ..vrobots_msgs.python.VROBOTS_CMDS import CMD_DICT
from .msg_helper import VRobotState


class WebsocketClient:
    def __init__(self, robot) -> None:
        self.robot = robot
        self.duration = 5.0

        def on_message(ws, message):
            # print("message recieved")
            # print(message)
            self.robot.unpack(message)

        def on_error(ws, error):
            print(error)

        def on_close(ws, close_status_code, close_msg):
            print("### closed ###")

        def on_open(ws):
            print("Opened connection")

            ## setup and send setup message
            self.robot.setup()
            byte_msg_list = self.robot.setup_msg_list
            if (byte_msg_list is not None):
                [ws.send(byte_msg, opcode=0x2) for byte_msg in byte_msg_list]

            def _update_loop(*args):
                while True:
                    if (
                        time.time() - self.robot.cmdMsgTReset.timestamp
                    ) > self.robot.duration:
                        break
                    time.sleep(0.02)  # 50 hz
                    self.robot.loop()
                    byte_msg_list = self.robot.pack()
                    if (byte_msg_list is not None):
                        [ws.send(byte_msg, opcode=0x2) for byte_msg in byte_msg_list]
                    # ws.send("hello server")

            _thread.start_new_thread(_update_loop, ())

        self.ws = websocket.WebSocketApp(
            "ws://localhost:12740",
            on_open=on_open,
            on_close=on_close,
            on_error=on_error,
            on_message=on_message,
        )

    def start(self):
        self.ws.run_forever()


class VirtualRobot(ABC):
    def __init__(self) -> None:
        self.setup = None
        self.loop = None
        self.cmdMsgT: CommandMsgT = CommandMsgT()
        self.cmdMsgTReset: CommandMsgT = CommandMsgT()
        self.cmdMsgTReset.name = "python"
        self.cmdMsgTReset.timestamp = time.time()
        self.cmdMsgTReset.id = CMD_DICT["reset_robot"]
        self.setup_msg_list = []

    def pack_cmd_reset(self) -> bytes:
        return self.Tobj2bytes(self.cmdMsgTReset)

    def Tobj2bytes(self, msgT):
        builder = flatbuffers.Builder(512)
        os = msgT.Pack(builder)
        builder.Finish(os, b"CMD0")
        return builder.Output()

    # Returns a list of byte messages that contains FBs
    @abstractmethod
    def pack_setup(self) -> [bytes]:  # type: ignore
        pass

    # Returns a list of byte messages that contains FBs
    @abstractmethod
    def pack(self) -> [bytes]:  # type: ignore
        pass

    def unpack(self, msg):
        objdata = StatesMsgT.InitFromPackedBuf(msg, 0)
        name = objdata.name.decode("utf-8")
        self.states = VRobotState(objdata)


class System:
    def __init__(
        self, robot, ubicoders_main_obj, duration=60.0, stop_condition=None
    ) -> None:
        self.robot = robot
        self.robot.setup = ubicoders_main_obj.setup
        self.robot.loop = ubicoders_main_obj.loop
        self.robot.duration = duration
        self.ws = WebsocketClient(self.robot)

    def start(self):
        self.ws.start()


if __name__ == "__main__":
    sys = System()

INITIALSTATE = 1  # 初始状态
DIGGING = 2  # 挖掘状态
CARRYING = 3  # 正在运送
READYTOLOAD = 4  # 准备装车
LOADINGDOUBT = 5  # 疑似装车
LOADINGCOMPLETE = 6  # 装车完毕


class ShudouState:
    def __init__(self):
        self.state = INITIALSTATE
        self.shudouCnt = 0
        self.disCnt = 0
        self.rec = None
        self.verticalCnt = 0
        self.horizontalCnt = 0
        self.noTruckCnt = 0
        self.douY = 0

    def set_state(self, state):
        self.state = state

    def init(self):
        # self.shudouCnt = 0
        self.disCnt = 0
        self.rec = None
        self.verticalCnt = 0
        self.horizontalCnt = 0
        self.noTruckCnt = 0
        self.douY = 0

import math


class RecResult:
    def __init__(self, x, y, l, h, label, conf):
        self.x = x
        self.y = y
        self.l = l
        self.h = h
        self.label = label
        self.conf = conf
        pass

    def get_bucket_state(self):
        # 获取斗的竖直水平状态 1为竖直 0为水平 -1不为斗
        if self.label[:5] == "Truck":
            return -1
        if self.label[6] == "0":
            return 0
        return 1

    def get_truck_state(self):
        # 获取卡车的状态
        pass

    def get_distance(self, a):
        # 获取斗与卡车的距离
        # 需要注意的是偶尔会有多个卡车的情况 这时候可以去选择距离最近的卡车？
        return math.sqrt((self.x - a.x) ** 2 + (self.y - a.y) ** 2)

    def get_intersection(self, a):
        # 水平范围是否相交
        lmx = max(self.x - self.l / 2, a.x - a.l / 2)
        rmi = min(self.x + self.l / 2, a.x + a.l / 2)
        return lmx < rmi

    def get_invlove(self, x):
        return self.x - self.l / 2 < x and self.x + self.l / 2 > x

from sensor import DroneSensor


class BigQuad(DroneSensor):
    def __init__(self):
        super().__init__()
        self.locate = [0, 0, 0]  # 맵에 따라 설정
        self.target = [0, 0, 0]  # 맵에 따라 설정
        self.vel = [0, 0, 0]  # 초기 0
        self.acc = [0, 0, 0]  # 초기 0
        self.ang = [0]  # 초기 0
        self.arrive = False
        self.stat_li = [self.locate, self.target, self.vel, self.acc, self.ang, self.arrive]

    def getState(self):
        return self.stat_li

    def setMotors(self, action, finish):
         self.updateState()

    def updateState(self):
        pass

    def giveReward(self, obstacle):
        reward = 0
        terminal = False

        for obs in obstacle:
            if obs <= 0:
                reward -= 150
                terminal = True
                return reward, terminal
            else:
                reward += 3

        dis_x = abs(self.target[0] - self.locate[0])
        dis_y = abs(self.target[1] - self.locate[1])
        dis_z = abs(self.target[2] - self.locate[2])

        if (dis_x+dis_y+dis_z) < 0.001:
            reward += 150
            terminal = True
            return reward, terminal

        reward = 70/dis_x + 70/dis_y + 70/dis_z

        return reward, terminal


if __name__ == '__main__':
    print("QuadDrone")

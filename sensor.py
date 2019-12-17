import math


class DroneSensor(object):
    def __init__(self):
        self.thr = [[-6, 6], [-6, 6], [-6, 6]]
        center_censor = [1, 0, 0]
        self.sensor_list = []
        self.sensor_list.append(center_censor)
        angle_1, angle_2 = math.pi / 6, math.pi / 3
        ang1_sensor = [center_censor[0] * math.cos(angle_1), center_censor[1], center_censor[2] * math.sin(angle_1)]
        ang2_sensor = [center_censor[0] * math.cos(angle_2), center_censor[1], center_censor[2] * math.sin(angle_2)]
        for i in range(0, 8):
            self.sensor_list.extend([ang1_sensor, ang2_sensor])
            ang1_sensor = self.rot45(ang1_sensor)
            ang2_sensor = self.rot45(ang2_sensor)

    def rot45(self, line):  # x축으로 45도 회전
        rot = math.cos(math.pi / 4)
        ret_line = [0, 0, 0]
        ret_line[0] = line[0]
        ret_line[1] = rot * line[1] - rot * line[2]
        ret_line[2] = rot * line[1] + rot * line[2]
        return ret_line

    def dist(self, obj_A, obj_B):
        sum = 0
        for i in range(0, 3):
            sum += pow(obj_A[i]-obj_B[i], 2.0)
        return pow(sum, 0.5)

    def sense(self, drone_angle, drone_crdn, obst_l):
        def rot_z(line, drone_angle):
            rotcos = math.cos(drone_angle)
            rotsin = math.sin(drone_angle)
            ret_line = [0, 0, 0]
            ret_line[2] = line[2]
            ret_line[0] = rotcos * line[0] - rotsin * line[1]
            ret_line[1] = rotsin * line[0] + rotcos * line[1]
            return ret_line

        def repair_foot(line, obj):
            nonlocal drone_angle, drone_crdn
            ret_crd = [0, 0, 0]
            a, b, c, l, m, n, x, y, z = obj[0], obj[1], obj[2], line[0], line[1],line[2], drone_crdn[0], drone_crdn[1], \
                                        drone_crdn[2]
            ld=((a-x)*l+(b-y)*m+(c-z)*n)/(l*l+m*m+n*n)
            for i in range(0,3):
                ret_crd[i]=drone_crdn[i]+line[i]*ld
            return ret_crd

        ret_list = [None] * 17
        for i in range(0, len(self.sensor_list)):
            line = rot_z(self.sensor_list[i], drone_angle)
            for obj in obst_l:
                crd = repair_foot(line, obj)
                dist = self.dist(crd, obj)
                if dist <= obj[3]:
                    ret_list[i] = self.dist(drone_crdn, crd)-pow(obj[3]**2-dist**2, 0.5)
                    break
            if ret_list[i] is None:
                wall, crd = [0] * 3, [0] * 3
                w_close, w_dis = 3, 100000
                for j in range(0, 3):
                    wall[j] = self.thr[j][0 if line[j] < 0 else 1]
                    tmp = (wall[j] - drone_crdn[j]) / line[j] if line[j] != 0 else 100000
                    if w_dis > tmp:
                        w_dis = tmp
                        w_close = j
                ld = (wall[w_close] - drone_crdn[w_close]) / line[w_close]
                for j in range(0, 3):
                    crd[j] = drone_crdn[j] + line[j] * ld
                ret_list[i] = self.dist(drone_crdn, crd)
        print(ret_list)
        return ret_list

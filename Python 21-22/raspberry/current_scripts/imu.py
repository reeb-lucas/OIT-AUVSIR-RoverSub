import time

GYRO: int = 0
POSITION: int = 1
YAW: int = 0
PITCH: int = 1
ROLL: int = 2
NORTH: int = 0
EAST: int = 1
DOWN: int = 2


class IMU:
    StringIn = ""
    Angle = [0.0, 0.0, 0.0]
    StartingAngle = [0.0, 0.0, 0.0]
    Position = [0.0, 0.0, 0.0]
    StartingPosition = [0.0, 0.0, 0.0]
    Acceleration = [0.0, 0.0, 0.0]
    AngularVelocity = [0.0, 0.0, 0.0]
    Velocity = [0.0, 0.0, 0.0]
    Measures = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    Error = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    Previous_Error = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    Error_Sum = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    Error_Delta = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    # gyro              position

    # this is a comment
    Kp = [[0.7, 0.5, 0.5], [0.3, 0.4, 0.4]]  # constant to modify PID
    Ki = [[0.0, 0.00, 0.00], [0.1, 0.1, 0.1]]  # constant to modify PID
    Kd = [[0.3, 0.3, 0.3], [0.1, 0.1, 0.1]]  # constant to modify PID

    North_PID = 0.0
    North_P = 0.0
    North_I = 0.0
    North_D = 0.0

    East_PID = 0.0
    East_P = 0.0
    East_I = 0.0
    East_D = 0.0

    Down_PID = 0.0
    Down_P = 0.0
    Down_I = 0.0
    Down_D = 0.0

    Yaw_PID = 0.0
    Yaw_P = 0.0
    Yaw_I = 0.0
    Yaw_D = 0.0

    Pitch_PID = 0.0
    Pitch_P = 0.0
    Pitch_I = 0.0
    Pitch_D = 0.0

    Roll_PID = 0.0
    Roll_P = 0.0
    Roll_I = 0.0
    Roll_D = 0.0

    def __init__(self, serial, id=0, name=""):

        # read info from vehicle
        self.serial = serial
        self.serial.flushInput()
        self.ID = id
        self.name = ""

        # arm vehicle to see position
        # print(self.serial.readline())
        # - Read the actual attitude: Roll, Pitch, and Yaw
        self.updateGyro()
        self.StartingAngle = self.Angle
        print('Orientation: ', self.getStartingGyro())

        # - Read the actual position North, East, and Down
        # self.UpdatePosition()
        # self.StartingPosition = self.Position
        # print('Position: ', self.getStartingPosition())

        # - Read the actual depth:
        time.sleep(3)
        print("Starting gyro: ", self.StartingAngle)
        # print("Starting position: ", self.Position)

    # gets hardware info
    def getInfo(self):
        return self.name

    # updates class with data from hardware
    def updateGyro(self):
        pass

    # position read when starting the RoboSub
    def getStartingPosition(self):
        return self.StartingPosition

    # current position read
    def getPosition(self):
        return self.Acceleration

    def getNorth(self):
        return self.Acceleration[NORTH]

    def getEast(self):
        return self.Acceleration[EAST]

    def getDown(self):
        return self.Acceleration[DOWN]

    # gyro read when starting the RoboSub
    def getStartingAngle(self):
        return self.StartingAngle

    # current gyro read
    def getAngle(self):
        return self.Angle

    def getPitch(self):
        return self.Angle[PITCH]

    def getRoll(self):
        return self.Angle[ROLL]

    def getYaw(self):
        return self.Angle[YAW]

    # req for PID calculation
    def CalculateError(self, yawoffset=0, pitchoffset=0, rolloffset=0, northoffset=0, eastoffset=0, downoffset=0):

        # previous error for error delta
        # gyro
        self.Previous_Error[GYRO][YAW] = self.Error[GYRO][YAW]
        self.Previous_Error[GYRO][PITCH] = self.Error[GYRO][PITCH]
        self.Previous_Error[GYRO][ROLL] = self.Error[GYRO][ROLL]

        # position
        self.Previous_Error[POSITION][NORTH] = self.Error[POSITION][NORTH]
        self.Previous_Error[POSITION][EAST] = self.Error[POSITION][EAST]
        self.Previous_Error[POSITION][DOWN] = self.Error[POSITION][DOWN]

        # error for proportional control
        # gyro
        if ((180 - abs(yawoffset)) + (180 - abs(self.Angle[YAW]))) < 180:
            self.Error[GYRO][YAW] = self.Angle[YAW] - yawoffset
        elif ((abs(yawoffset)) + (abs(self.Angle[YAW]))) < 180:
            self.Error[GYRO][YAW] = self.Angle[YAW] + yawoffset
        self.Error[GYRO][PITCH] = self.Angle[PITCH] - pitchoffset
        self.Error[GYRO][ROLL] = self.Angle[ROLL] - rolloffset

        # position
        self.Error[POSITION][NORTH] = self.Acceleration[NORTH] - northoffset
        self.Error[POSITION][EAST] = self.Acceleration[EAST] - eastoffset
        self.Error[POSITION][DOWN] = self.Acceleration[DOWN] - downoffset

        # sum of error for integral
        # gyro
        self.Error_Sum[GYRO][YAW] = self.Error_Sum[GYRO][YAW] + self.Error[GYRO][YAW]
        self.Error_Sum[GYRO][PITCH] = self.Error_Sum[GYRO][PITCH] + self.Error[GYRO][PITCH]
        self.Error_Sum[GYRO][ROLL] = self.Error_Sum[GYRO][ROLL] + self.Error[GYRO][ROLL]

        # position
        self.Error_Sum[POSITION][NORTH] = self.Error_Sum[POSITION][NORTH] + self.Error[POSITION][NORTH]
        self.Error_Sum[POSITION][EAST] = self.Error_Sum[POSITION][EAST] + self.Error[POSITION][EAST]
        self.Error_Sum[POSITION][DOWN] = self.Error_Sum[POSITION][DOWN] + self.Error[POSITION][DOWN]

        # math for change in error to do derivative
        # gyro
        self.Error_Delta[GYRO][YAW] = self.Error[GYRO][YAW] - self.Previous_Error[GYRO][YAW]
        self.Error_Delta[GYRO][PITCH] = self.Error[GYRO][PITCH] - self.Previous_Error[GYRO][PITCH]
        self.Error_Delta[GYRO][ROLL] = self.Error[GYRO][ROLL] - self.Previous_Error[GYRO][ROLL]

        # position
        self.Error_Delta[POSITION][NORTH] = self.Error[POSITION][NORTH] - self.Previous_Error[POSITION][NORTH]
        self.Error_Delta[POSITION][EAST] = self.Error[POSITION][EAST] - self.Previous_Error[POSITION][EAST]
        self.Error_Delta[POSITION][DOWN] = self.Error[POSITION][DOWN] - self.Previous_Error[POSITION][DOWN]

    # pid calculation
    def CalculatePID(self):
        # Yaw PID variable setting
        self.Yaw_P = (self.Error[GYRO][YAW] * self.Kp[GYRO][YAW])
        self.Yaw_I = (self.Error_Sum[GYRO][YAW] * self.Ki[GYRO][YAW])
        self.Yaw_D = (self.Error_Delta[GYRO][YAW] * self.Kd[GYRO][YAW])
        self.Yaw_PID = self.Yaw_P + self.Yaw_I + self.Yaw_D

        # Pitch PID variable setting
        self.Pitch_P = (self.Error[GYRO][PITCH] * self.Kp[GYRO][PITCH])
        self.Pitch_I = (self.Error_Sum[GYRO][PITCH] * self.Ki[GYRO][PITCH])
        self.Pitch_D = (self.Error_Delta[GYRO][PITCH] * self.Kd[GYRO][PITCH])
        self.Pitch_PID = self.Pitch_P + self.Pitch_I + self.Pitch_D

        # Roll PID variable setting
        self.Roll_P = (self.Error[GYRO][ROLL] * self.Kp[GYRO][ROLL])
        self.Roll_I = (self.Error_Sum[GYRO][ROLL] * self.Ki[GYRO][ROLL])
        self.Roll_D = (self.Error_Delta[GYRO][ROLL] * self.Kd[GYRO][ROLL])
        self.Roll_PID = self.Roll_P + self.Roll_I + self.Roll_D

        # North PID variable setting
        self.North_P = (self.Error[POSITION][NORTH] * self.Kp[POSITION][NORTH])
        self.North_I = (self.Error_Sum[POSITION][NORTH] * self.Ki[POSITION][NORTH])
        self.North_D = (self.Error_Delta[POSITION][NORTH] * self.Kd[POSITION][NORTH])
        self.North_PID = self.North_P  # + self.North_I + self.North_D

        # East PID variable setting
        self.East_P = (self.Error[POSITION][EAST] * self.Kp[POSITION][EAST])
        self.East_I = (self.Error_Sum[POSITION][EAST] * self.Ki[POSITION][EAST])
        self.East_D = (self.Error_Delta[POSITION][EAST] * self.Kd[POSITION][EAST])
        self.East_PID = self.East_P  # + self.East_I + self.East_D

        # Down PID variable setting
        self.Down_P = (self.Error[POSITION][DOWN] * self.Kp[POSITION][DOWN])
        self.Down_I = (self.Error_Sum[POSITION][DOWN] * self.Ki[POSITION][DOWN])
        self.Down_D = (self.Error_Delta[POSITION][DOWN] * self.Kd[POSITION][DOWN])
        self.Down_PID = self.Down_P  # + self.Down_I + self.Down_D

    def getYawPID(self):
        return self.Yaw_PID

    def getPitchPID(self):
        return self.Pitch_PID

    def getRollPID(self):
        return self.Roll_PID

    def getNorthPID(self):
        return self.Yaw_PID

    def getEastPID(self):
        return self.Pitch_PID

    def getDownPID(self):
        return self.Roll_PID

    def getPosition(self):
        return self.Position

    def getAcceleration(self):
        return self.Acceleration


class IMU_Group(IMU):
    IMU_count: int = 0

    def __init__(self, imulist=[]):
        # read info from vehicle
        self.IMU_list = imulist
        self.IMU_count = len(self.IMU_list)
        self.name = "Swarm"
        # arm vehicle to see position
        # print(self.serial.readline())
        # - Read the actual attitude: Roll, Pitch, and Yaw
        self.updateGyro()
        self.StartingAngle = self.Angle
        print('Orientation: ', self.getStartingGyro())

        # - Read the actual position North, East, and Down
        # self.UpdatePosition()
        # self.StartingPosition = self.Position
        # print('Position: ', self.getStartingPosition())

        # - Read the actual depth:
        time.sleep(3)
        print("Starting gyro: ", self.StartingAngle)
        # print("Starting position: ", self.Position)

    # updates class with data from hardware
    def updateGyro(self):
        i = 0
        temp = []
        self.Angle = list(self.Angle)
        # real shite workaround. whatever.
        for imu in self.IMU_list:
            # print("Updating group-gyro.")
            imu.updateGyro()
            temp = imu.getGyro()
            temp = list(temp)
            print("Temp(gyro-", i, ") readout: ", temp)
            if i == 0:
                self.Angle = temp
            else:
                j = 0
                for j in range(len(temp)):
                    self.Angle[j] += temp[j]
                    j += 1

            i += 1
        for data in self.Angle:
            data /= i
        self.Angle = tuple(self.Angle)
        return self.Angle

    def getGyro(self):
        return self.Angle

    # gyro read when starting the RoboSub
    def getStartingGyro(self):
        return self.StartingAngle

    def updatePosition(self):
        i = 0
        temp = []
        self.Position = list(self.Position)
        for imu in self.IMU_list:
            imu.updatePosition()
            temp = imu.getPosition()
            temp = list(temp)
            if i == 0:
                self.Position = temp
            else:
                j = 0
                for j in range(len(temp)):
                    self.Position[j] += temp[j]
                    j += 1

            i += 1
        for data in self.Position:
            data /= i
        self.Position = tuple(self.Position)
        return self.Position

    # current position read
    def getPosition(self):
        return self.Position

    # position read when starting the RoboSub
    def getStartingPosition(self):
        return self.StartingPosition

    # acceleration read
    def getAcceleration(self):
        return self.Acceleration

    def getNorth(self):
        return self.Position[NORTH]

    def getEast(self):
        return self.Position[EAST]

    def getDown(self):
        return self.Position[DOWN]

    def getPitch(self):
        return self.Angle[PITCH]

    def getRoll(self):
        return self.Angle[ROLL]

    def getYaw(self):
        return self.Angle[YAW]

    # req for PID calculation
    def CalculateError(self, yawoffset, pitchoffset, rolloffset, northoffset, eastoffset, downoffset):

        # previous error for error delta
        # gyro
        self.Previous_Error[GYRO][YAW] = self.Error[GYRO][YAW]
        self.Previous_Error[GYRO][PITCH] = self.Error[GYRO][PITCH]
        self.Previous_Error[GYRO][ROLL] = self.Error[GYRO][ROLL]

        # position
        self.Previous_Error[POSITION][NORTH] = self.Error[POSITION][NORTH]
        self.Previous_Error[POSITION][EAST] = self.Error[POSITION][EAST]
        self.Previous_Error[POSITION][DOWN] = self.Error[POSITION][DOWN]

        # error for proportional control
        # gyro
        if ((180 - abs(yawoffset)) + (180 - abs(self.Angle[YAW]))) < 180:
            self.Error[GYRO][YAW] = self.Angle[YAW] - yawoffset
        elif ((abs(yawoffset)) + (abs(self.Angle[YAW]))) < 180:
            self.Error[GYRO][YAW] = self.Angle[YAW] + yawoffset
        self.Error[GYRO][PITCH] = self.Angle[PITCH] - pitchoffset
        self.Error[GYRO][ROLL] = self.Angle[ROLL] - rolloffset

        # print("Yaw, Roll, Pitch error: ", self.Error[GYRO][YAW],
        #       self.Error[GYRO][PITCH],
        #       self.Error[GYRO][ROLL])

        # position
        self.Error[POSITION][NORTH] = self.Acceleration[NORTH] - northoffset
        self.Error[POSITION][EAST] = self.Acceleration[EAST] - eastoffset
        self.Error[POSITION][DOWN] = self.Acceleration[DOWN] - downoffset

        # sum of error for integral
        # gyro
        self.Error_Sum[GYRO][YAW] = self.Error_Sum[GYRO][YAW] + self.Error[GYRO][YAW]
        self.Error_Sum[GYRO][PITCH] = self.Error_Sum[GYRO][PITCH] + self.Error[GYRO][PITCH]
        self.Error_Sum[GYRO][ROLL] = self.Error_Sum[GYRO][ROLL] + self.Error[GYRO][ROLL]

        # position
        self.Error_Sum[POSITION][NORTH] = self.Error_Sum[POSITION][NORTH] + self.Error[POSITION][NORTH]
        self.Error_Sum[POSITION][EAST] = self.Error_Sum[POSITION][EAST] + self.Error[POSITION][EAST]
        self.Error_Sum[POSITION][DOWN] = self.Error_Sum[POSITION][DOWN] + self.Error[POSITION][DOWN]

        # math for change in error to do derivative
        # gyro
        self.Error_Delta[GYRO][YAW] = self.Error[GYRO][YAW] - self.Previous_Error[GYRO][YAW]
        self.Error_Delta[GYRO][PITCH] = self.Error[GYRO][PITCH] - self.Previous_Error[GYRO][PITCH]
        self.Error_Delta[GYRO][ROLL] = self.Error[GYRO][ROLL] - self.Previous_Error[GYRO][ROLL]

        # position
        self.Error_Delta[POSITION][NORTH] = self.Error[POSITION][NORTH] - self.Previous_Error[POSITION][NORTH]
        self.Error_Delta[POSITION][EAST] = self.Error[POSITION][EAST] - self.Previous_Error[POSITION][EAST]
        self.Error_Delta[POSITION][DOWN] = self.Error[POSITION][DOWN] - self.Previous_Error[POSITION][DOWN]

    # pid calculation
    def CalculatePID(self):
        # Yaw PID variable setting
        self.Yaw_P = (self.Error[GYRO][YAW] * self.Kp[GYRO][YAW])
        self.Yaw_I = (self.Error_Sum[GYRO][YAW] * self.Ki[GYRO][YAW])
        self.Yaw_D = (self.Error_Delta[GYRO][YAW] * self.Kd[GYRO][YAW])
        self.Yaw_PID = self.Yaw_P + self.Yaw_I + self.Yaw_D

        # Pitch PID variable setting
        self.Pitch_P = (self.Error[GYRO][PITCH] * self.Kp[GYRO][PITCH])
        self.Pitch_I = (self.Error_Sum[GYRO][PITCH] * self.Ki[GYRO][PITCH])
        self.Pitch_D = (self.Error_Delta[GYRO][PITCH] * self.Kd[GYRO][PITCH])
        self.Pitch_PID = self.Pitch_P + self.Pitch_I + self.Pitch_D

        # Roll PID variable setting
        self.Roll_P = (self.Error[GYRO][ROLL] * self.Kp[GYRO][ROLL])
        self.Roll_I = (self.Error_Sum[GYRO][ROLL] * self.Ki[GYRO][ROLL])
        self.Roll_D = (self.Error_Delta[GYRO][ROLL] * self.Kd[GYRO][ROLL])
        self.Roll_PID = self.Roll_P + self.Roll_I + self.Roll_D

        # test
        # print("Yaw, Pitch, Roll PID: ", self.Yaw_PID, self.Pitch_PID, self.Roll_PID)
        # North PID variable setting
        self.North_P = (self.Error[POSITION][NORTH] * self.Kp[POSITION][NORTH])
        self.North_I = (self.Error_Sum[POSITION][NORTH] * self.Ki[POSITION][NORTH])
        self.North_D = (self.Error_Delta[POSITION][NORTH] * self.Kd[POSITION][NORTH])
        self.North_PID = self.North_P  # + self.North_I + self.North_D

        # East PID variable setting
        self.East_P = (self.Error[POSITION][EAST] * self.Kp[POSITION][EAST])
        self.East_I = (self.Error_Sum[POSITION][EAST] * self.Ki[POSITION][EAST])
        self.East_D = (self.Error_Delta[POSITION][EAST] * self.Kd[POSITION][EAST])
        self.East_PID = self.East_P  # + self.East_I + self.East_D

        # Down PID variable setting
        self.Down_P = (self.Error[POSITION][DOWN] * self.Kp[POSITION][DOWN])
        self.Down_I = (self.Error_Sum[POSITION][DOWN] * self.Ki[POSITION][DOWN])
        self.Down_D = (self.Error_Delta[POSITION][DOWN] * self.Kd[POSITION][DOWN])
        self.Down_PID = self.Down_P  # + self.Down_I + self.Down_D

    def getYawPID(self):
        return self.Yaw_PID

    def getPitchPID(self):
        return self.Pitch_PID

    def getRollPID(self):
        return self.Roll_PID

    def getNorthPID(self):
        return self.Yaw_PID

    def getEastPID(self):
        return self.Pitch_PID

    def getDownPID(self):
        return self.Roll_PID

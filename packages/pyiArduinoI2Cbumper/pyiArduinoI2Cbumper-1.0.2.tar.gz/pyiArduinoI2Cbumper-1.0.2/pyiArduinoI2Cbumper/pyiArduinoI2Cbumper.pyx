# distutils: language = c++
# cython: language_level = 3

from iarduino_I2C_Bumper cimport iarduino_I2C_Bumper
#from time import sleep

DEF_CHIP_ID_FLASH          = 0x3C
DEF_CHIP_ID_METRO          = 0xC3
DEF_MODEL_BUM              = 0x10
# Адреса регистров модуля:
REG_FLAGS_0                = 0x00
REG_BITS_0                 = 0x01
REG_FLAGS_1                = 0x02
REG_BITS_1                 = 0x03
REG_MODEL                  = 0x04
REG_VERSION                = 0x05
REG_ADDRESS                = 0x06
REG_CHIP_ID                = 0x07
REG_BUM_FLG_LINE           = 0x10
REG_BUM_BIT_LAMP           = 0x12
REG_BUM_CALIBRATION        = 0x13
REG_BUM_THRESHOLD          = 0x14
REG_BUM_ANALOG             = 0x26
# Позиция битов и флагов:
BUM_FLG_LINE_BLACK         = 0x80
BUM_SET_HEAD_ON            = 0x80
BUM_SET_TURN_AUTO_STOP     = 0x60
BUM_SET_TURN_AUTO_STOP_0   = 0B00000000
BUM_SET_TURN_AUTO_STOP_1   = 0B00100000
BUM_SET_TURN_AUTO_STOP_2   = 0B01000000
BUM_SET_TURN_AUTO_STOP_3   = 0B01100000
BUM_SET_TURN_PERIOD        = 0x18
BUM_SET_TURN_PERIOD_100    = 0B00000000
BUM_SET_TURN_PERIOD_200    = 0B00001000
BUM_SET_TURN_PERIOD_400    = 0B00010000
BUM_SET_TURN_PERIOD_800    = 0B00011000
BUM_SET_TURN_MODE          = 0x07
BUM_SET_TURN_MODE_OFF      = 0B00000000
BUM_SET_TURN_MODE_LEFT     = 0B00000001
BUM_SET_TURN_MODE_RIGHT    = 0B00000010
BUM_SET_TURN_MODE_EMERGENCY= 0B00000011
BUM_SET_TURN_MODE_POLICE   = 0B00000100
BUM_SET_TURN_MODE_AUTO_1   = 0B00000101
BUM_SET_TURN_MODE_AUTO_2   = 0B00000110
BUM_SET_TURN_MODE_AUTO_3   = 0B00000111
BUM_FLG_CALIBRATION        = 0x80
BUM_STAGE_CALIBRATION      = 0x60
BUM_STAGE_OFF              = 0B00000000
BUM_STAGE_READ_LN          = 0B00100000
BUM_STAGE_WAITING          = 0B01000000
BUM_STAGE_READ_BG          = 0B01100000
BUM_SET_CALIBRATION        = 0x1F
BUM_CALIBR_RUN             = 0B00011011
BUM_CALIBR_END             = 0B00001001
BUM_CALIBR_END_A           = 0B00010010

BUM_STAGE_OFF_OK           = 0B10000000
BUM_STAGE_OFF_ERR          = 0B00000000

BUM_TURN_OFF               = 0
BUM_TURN_LEFT              = 1
BUM_TURN_RIGHT             = 2
BUM_TURN_EMERGENCY         = 3
BUM_TURN_POLICE            = 4
BUM_TURN_AUTO              = 5
BUM_TURN_100               = 6
BUM_TURN_200               = 7
BUM_TURN_400               = 8
BUM_TURN_800               = 9
BUM_AUTO_ON_1              = 10
BUM_AUTO_ON_2              = 11
BUM_AUTO_ON_3              = 12
BUM_AUTO_OFF_ANY           = 13
BUM_AUTO_OFF_CEN           = 14
BUM_LINE_ALL               = 15
BUM_LINE_WHITE             = 2
BUM_LINE_BLACK             = 3
BUM_LINE_CHANGE            = 4

NO_BEGIN = 1

cdef class pyiArduinoI2Cbumper:
    cdef iarduino_I2C_Bumper c_module

    def __cinit__(self, address=None, auto=None):

        if address is not None:

            self.c_module = iarduino_I2C_Bumper(address)

            if auto is None:
                #sleep(.5)
                if not self.c_module.begin():

                    print("ошибка инициализации модуля.\n"
                          "Проверьте подключение и адрес модуля,"
                          " возможно не включен интерфейс I2C.\n"
                          " Запустите raspi-config и включите интерфейс"
                          ", инструкция по включению:"
                          " https://wiki.iarduino.ru/page/raspberry-i2c-spi/")

        else:

            self.c_module = iarduino_I2C_Bumper()

            if auto is None:
                #sleep(.5)
                if not self.c_module.begin():

                    print("ошибка инициализации модуля.\n"
                          "Проверьте подключение и адрес модуля, "
                          " возможно не включен интерфейс I2C.\n"
                          " Запустите raspi-config и включите интерфейс"
                          ", инструкция по включению:"
                          " https://wiki.iarduino.ru/page/raspberry-i2c-spi/")

    def begin(self):
        return self.c_module.begin()

    def changeAddress(self, unsigned char newAddr):
        return self.c_module.changeAddress(newAddr)

    def reset(self):
        return self.c_module.reset()

    def getAddress(self):
        return self.c_module.getAddress()

    def getVersion(self):
        return self.c_module.getVersion()

    def getPullI2C(self):
        return self.c_module.getPullI2C()

    def setPullI2C(self, flag=None):
        if flag is not None:
            return self.c_module.setPullI2C(flag)
        else:
            return self.c_module.setPullI2C(True)

    def setLamp(self, state):
        return self.c_module.setLamp(state)

    def setTurnSignal(self, mode):
        return self.c_module.setTurnSignal(mode)

    def setTurnPeriod(self, period):
        return self.c_module.setTurnPeriod(period)

    def settingsTurnAuto(self, start, stop, flag=None):

        if flag is not None:

            return self.c_module.settingsTurnAuto(start, stop, flag)

        else:

            return self.c_module.settingsTurnAuto(start, stop, False)

    def setCalibrationRun(self):
        return self.c_module.setCalibrationRun()

    def setCalibrationEnd(self, flag=None):
        if flag is not None:
            return self.c_module.setCalibrationEnd(flag)
        else:
            return self.c_module.setCalibrationEnd(False)

    def setCalibrationManual(
                                self,
                                adc_1 = None, adc_2 = None, adc_3 = None,
                                adc_4 = None, adc_5 = None, adc_6 = None,
                                adc_7 = None, adc_8 = None, adc_9 = None
                                                    ):
        if adc_2 is not None:

            return self.c_module.setCalibrationManual(
                                                        adc_1, adc_2, adc_3,
                                                        adc_4, adc_5, adc_6,
                                                        adc_7, adc_8, adc_9
                                                                            )

        else:

            return self.c_module.setCalibrationManualOverloaded(adc_1)

    def getCalibrationStage(self):
        return self.c_module.getCalibrationStage()

    def getLineDigital(self, num):
        return self.c_module.getLineDigital(num)

    def getLineAnalog(self, num):
        return self.c_module.getLineAnalog(num)

    def getErrPID(self):
        return self.c_module.getErrPID()

    # getting number of activated sensors
    # and activated sensor bits, passed by ref in c++
    cpdef getLineSum(self, a=None):

        # var to be passed (have to be c-defed)
        cdef unsigned short activeSensorBits = 0

        # python's crappy way of overloading.
        # (Yes, I know about "overloading" module
        # it is not installed by default and I
        # don't want people to install more stuff...
        # sed 11q 😱😱😱)
        if a is not None:

            nSens = self.c_module.getLineSumOverloaded(activeSensorBits)

            return nSens, activeSensorBits

        else:

            return self.c_module.getLineSum()

    def getLineType(self):
        return self.c_module.getLineType()

    def setLineType(self, line_type):
        return self.c_module.setLineType(line_type)

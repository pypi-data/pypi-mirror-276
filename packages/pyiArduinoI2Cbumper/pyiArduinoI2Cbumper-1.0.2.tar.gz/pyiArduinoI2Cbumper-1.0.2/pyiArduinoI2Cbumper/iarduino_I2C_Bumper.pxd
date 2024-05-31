cdef extern from "iarduino_I2C_Bumper.cpp":
    pass

cdef extern from "iarduino_I2C_Bumper.h":
    cdef cppclass iarduino_I2C_Bumper:
        iarduino_I2C_Bumper() except +
        iarduino_I2C_Bumper(unsigned char) except +
        bint begin()
        bint changeAddress(unsigned char)
        bint reset()
        unsigned char getAddress()
        unsigned char getVersion()
        bint getPullI2C()
        bint setPullI2C(bint)
        bint setLamp(bint)
        bint setTurnSignal(unsigned char)
        bint setTurnPeriod(unsigned char)
        bint settingsTurnAuto(unsigned char, unsigned char, bint)
        bint setCalibrationRun()
        bint setCalibrationEnd(bint)
        bint setCalibrationManual(unsigned short,unsigned short,unsigned short,unsigned short,unsigned short,unsigned short,unsigned short,unsigned short,unsigned short)
        bint setCalibrationManualOverloaded "setCalibrationManual"(unsigned short)
        unsigned char getCalibrationStage()
        unsigned short getLineDigital(unsigned char)
        unsigned short getLineAnalog(unsigned char)
        float getErrPID()
        unsigned char getLineSum()
        unsigned char getLineSumOverloaded "getLineSum"(unsigned short)
        unsigned char getLineType()
        bint setLineType(unsigned char)

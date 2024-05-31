# ПРИМЕР УПРАВЛЕНИЯ ПОВОРОТНИКАМИ НА БАМПЕРЕ:

from time import sleep

#   Подключаем библиотеку для работы с бампером I2C-flash.
from pyiArduinoI2Cbumper import *

#   Объявляем объект bum для работы с функциями и методами библиотеки
#   pyiArduinoI2Cbumper, указывая адрес модуля на шине I2C.
#   Если объявить объект без указания адреса bum = pyiArduinoI2Cbumper(),
#   то адрес будет найден автоматически.
bum = pyiArduinoI2Cbumper(0x09)

# Задаём скорость мигания поворотников в 400мс.
# Возможные значения: BUM_TURN_100, BUM_TURN_200, BUM_TURN_400 и BUM_TURN_800.
bum.setTurnPeriod(BUM_TURN_400)

while True:

    #   Включаем левый поворотник.
    bum.setTurnSignal(BUM_TURN_LEFT)
    sleep(5)

    #   Включаем правый поворотник.
    bum.setTurnSignal(BUM_TURN_RIGHT)
    sleep(5)

    #   Включаем поворотниками аварийный сигнал.
    bum.setTurnSignal(BUM_TURN_EMERGENCY)
    sleep(5)

    #   Включаем поворотники в полицейский режим.
    bum.setTurnSignal(BUM_TURN_POLICE)
    sleep(5)

    #   Отключаем поворотники.
    bum.setTurnSignal(BUM_TURN_OFF)
    sleep(5)

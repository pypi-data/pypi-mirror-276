# ПРИМЕР ПОЛУЧЕНИЯ И УКАЗАНИЯ ТИПА ЛИНИИ ТРАССЫ:

# Тип линии, равно как и калибровочные значения,
# хранятся в энергонезависимой памяти модуля.

from time import sleep

#   Подключаем библиотеку для работы с бампером I2C-flash.
from pyiArduinoI2Cbumper import *

#   Объявляем объект bum для работы с функциями и методами
#   библиотеки pyiArduinoI2Cbumper, указывая адрес модуля на шине I2C.
#   Если объявить объект без указания адреса bum = pyiArduinoI2Cbumper(),
#   то адрес будет найден автоматически.
bum = pyiArduinoI2Cbumper(0x09)

while True:

#  ОПРЕДЕЛЯЕМ ИСПОЛЬЗУЕМЫЙ ТИП ЛИНИИ:
    if bum.getLineType() == BUM_LINE_BLACK:
        first = "тёмной"
        second = "светлой"
    elif bum.getLineType() == BUM_LINE_WHITE:
        first = "светлой"
        second = "тёмной"

    t = "Модуль использовал трассу с {} линией"\
        ", а теперь использует трассу"\
        "с {} линией".format(first, second)

    print(t)

#  УКАЗЫВАЕМ НОВЫЙ ТИП ЛИНИИ:
#  Тип линии задаётся как BUM_LINE_BLACK - тёмная
#  BUM_LINE_WHITE - светлая
#  BUM_LINE_CHANGE - сменить тип линии.
    bum.setLineType(BUM_LINE_CHANGE)

    sleep(2)

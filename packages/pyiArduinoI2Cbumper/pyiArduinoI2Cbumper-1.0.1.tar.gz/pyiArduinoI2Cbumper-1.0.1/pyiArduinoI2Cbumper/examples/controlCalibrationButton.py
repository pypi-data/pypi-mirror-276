# Пример контроля за калибровкой бампера кнопкой:           #

#  ПЕРЕЧЕНЬ ЗНАЧЕНИЙ   возвращаемых функцией getCalibrationStage():
#  BUM_STAGE_READ_LN - выполняется чтение АЦП с датчиков установленных над линией трассы.
#  BUM_STAGE_WAITING - модуль ожидает поступления команды на чтение фона.
#  BUM_STAGE_READ_BG - выполняется чтение АЦП с датчиков установленных над фоном трассы.
#  BUM_STAGE_OFF_ERR - калибровка завершена провалом.
#  BUM_STAGE_OFF_OK  - калибровка завершена успехом.

#   Подключаем библиотеку для работы с бампером I2C-flash.
from pyiArduinoI2Cbumper import *

#   Объявляем объект bum для работы с функциями и методами библиотеки pyiArduinoI2Cbumper, указывая адрес модуля на шине I2C.
bum = pyiArduinoI2Cbumper(0x09)

print("Установите бампер над линией трассы")
print("Нажмите на кнопку «калибровка».")

#   Ждём начала чтения показаний с линий трассы.
while bum.getCalibrationStage() != BUM_STAGE_READ_LN:
    pass

print("Выполняется чтение линий трассы...")

#   Ждём перехода модуля в стадию ожидания команды на чтение фона.
while bum.getCalibrationStage() != BUM_STAGE_WAITING:
    pass

print("Чтение линий завершено.\r\n")
print("Установите бампер над фоном трассы")
print("Нажмите на кнопку «калибровка».\r\n")

#   Ждём начала чтения показаний с фона трассы.
while bum.getCalibrationStage() != BUM_STAGE_READ_BG:
    pass

print("Выполняется чтение фона трассы...")

#   Ждём завершения чтения показаний с фона трассы.
while bum.getCalibrationStage() == BUM_STAGE_READ_BG:
    pass

print("Чтение фона завершено.\r\n")

#   Если калибровка выполнена успешно, то...
if bum.getCalibrationStage() == BUM_STAGE_OFF_OK:
    print("Калибровка выполнена успешно!")
else:
    print("Калибровка не выполнена!")

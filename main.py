from ppadb.client import Client as AdbClient
from time import sleep
import datetime

client = AdbClient(host="127.0.0.1", port=5037)

client.remote_connect("172.24.62.148", 5555)  # подсоединяем девайсы по adb via wifi
client.remote_connect("172.24.62.149", 5555)

devices = client.devices()

i = 0
iter_count = 10  # Количество промежутков для измерения

while i != iter_count:
    for device in devices:
        print(str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute))
        print('device ' + str(device.get_serial_no()))
        print('battery ' + str(device.get_battery_level()))

        sleep(1)  # интервал в 10 минут

    i += 1

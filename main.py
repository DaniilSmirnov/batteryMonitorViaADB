from ppadb.client import Client as AdbClient
from time import sleep
import datetime

client = AdbClient(host="127.0.0.1", port=5037)

client.remote_connect("172.24.62.148", 5555)  # подсоединяем девайсы по adb via wifi
client.remote_connect("172.24.62.148", 5555)

devices = client.devices()

i = 0
iter_count = 10  # Количество промежутков для измерения

for device in devices:

    if i == iter_count:
        break

    print(str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute))
    print(device.get_serial_no())
    print(device.get_battery_level())

    i += 1
    sleep(600)  # интервал в 10 минут

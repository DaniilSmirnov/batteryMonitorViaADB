from ppadb.client import Client as AdbClient
import matplotlib.pyplot as plt
from time import sleep
import datetime
import os

from database import update_device_state, get_devices_state

client = AdbClient(host="127.0.0.1", port=5037)

# client.remote_connect("172.24.62.148", 5555)  # подсоединяем девайсы по adb via wifi
# client.remote_connect("172.24.62.149", 5555)

connected_devices = client.devices()

i = 0
iter_count = 2  # Количество промежутков для измерения
minutes = 1  # Количество минут между измерениями

while i != iter_count:
    for device in connected_devices:
        update_device_state(str(device.get_serial_no()),
                            str(device.get_battery_level()),
                            str(device.cpu_percent()),
                            str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute))

    sleep(60 * minutes)

    i += 1

for device in connected_devices:
    serial = device.get_serial_no()
    x, y = get_devices_state(serial)
    plt.plot(x, y, label=('device ' + str(serial)))

plt.xlabel('Время')
plt.ylabel('Значения')
plt.legend()
plt.show()

os.remove("stats.db")

from ppadb.client import Client as AdbClient
import matplotlib.pyplot as plt
from time import sleep
import datetime
import os

from database import update_device_state, get_devices_state

iter_count = 30  # Количество промежутков для измерения
minutes = 1  # Количество минут между измерениями

client = AdbClient(host="127.0.0.1", port=5037)
# client.remote_connect("172.24.62.148", 5555)  # подсоединяем девайсы по adb via wifi
# client.remote_connect("172.24.62.149", 5555)

os.remove("stats.db")
connected_devices = client.devices()
i = 0

print("Started at {0}:{1}".format(datetime.datetime.now().hour, datetime.datetime.now().minute))
while i != iter_count:
    for device in connected_devices:
        update_device_state(str(device.get_serial_no()),
                            str(device.get_battery_level()),
                            str(device.cpu_percent()),
                            str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute))
    print("Iteration {0}/{1} updated state".format(i, iter_count))
    sleep(60 * minutes)

    i += 1

print('Generating plot')
for device in connected_devices:
    serial = device.get_serial_no()
    x, y = get_devices_state(serial)
    plt.plot(x, y, label=('device ' + str(serial)))

plt.xlabel('Время')
plt.ylabel('Значения')
plt.legend()
fig = plt.gcf()
plt.show()
fig.savefig(str(datetime.datetime.now()) + '.png')

os.remove("stats.db")

import sqlite3


def get_conn():
    conn = sqlite3.connect('stats.db')
    return conn, conn.cursor()


def create_db():
    print('recreate')

    conn, cursor = get_conn()

    cursor.execute('''
    CREATE TABLE "statistics" (
	"device_serial"	TEXT,
	"battery"	TEXT,
	"processor"	TEXT,
	"time"	TEXT
);
    ''')

    conn.commit()


def update_device_state(device, battery, processor, time):
    conn, cursor = get_conn()
    query = "insert into statistics values (?, ?, ?, ?)"
    data = (device, battery, processor, time)
    try:
        cursor.execute(query, data)
        conn.commit()
    except sqlite3.OperationalError:
        create_db()
        update_device_state(device, battery, processor, time)


def get_devices_state(device):
    conn, cursor = get_conn()
    query = "select battery, processor, time from statistics where device_serial = ? order by time asc"
    data = (str(device),)
    cursor.execute(query, data)

    rawdata = get_array(cursor, get_column_names(cursor.description))

    battery = []
    time = []
    for data in rawdata:
        battery.append(data.get('battery'))
        time.append(data.get('time'))

    return time, battery


def get_array(cursor, keys):
    keys = list(keys)
    response = []

    data = cursor.fetchone()
    while data is not None:
        response.append(dict(zip(keys, data)))
        data = cursor.fetchone()

    return response


def get_column_names(colnames):
    response = []
    for row in colnames:
        response.append(row[0])

    return response

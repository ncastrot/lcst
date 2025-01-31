#########################################################################
# to average every data every one minute of the lcst                    #
#########################################################################

import pandas as pd
from datetime import datetime

files = "file.txt"
header = ["date", "time", "bcc_sensor", "bcc", "bba_sensor", "bba1", "bba2", "lux", "lux_white", "lux_g", "lux_it", "uva", "uvb", "uv_bool", "uvc", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "t11", "t12", "t13", "t14", "t15", "t16", "t17", "t18", "t19", "t20", "temp", "press", "hum"]

# load data
data = pd.read_csv(f"/path/to/the/raw/file/{files}", header=None, names=header)

# combine date and time columns into a single datetime column
data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time'])

# set datetime as the index
data.set_index('datetime', inplace=True)

# resample data to one-minute intervals and calculate the mean for each minute
data_minute_avg = data.resample('1T').mean()

# drop rows where there are no data points within the minute
data_minute_avg.dropna(inplace=True)

# reset index to separate date and time
data_minute_avg.reset_index(inplace=True)

# split datetime back to date and time
data_minute_avg['date'] = data_minute_avg['datetime'].dt.date
data_minute_avg['time'] = data_minute_avg['datetime'].dt.time

# save only the needed/interest data
data_minute_avg = data_minute_avg[['date', 'time', 'bcc', 'bba1', 'bba2', 'lux', 'lux_white', 'uva', 'uvb', 't1', 't2','t3', 't4','t5', 't6','t7', 't8','t9', 't10','t11', 't12','t13', 't14','t15', 't16','t17', 't18','t19', 't20', 'temp', 'press', 'hum']]

data_minute_avg.to_csv(f"/path/to/the/average/files/{files}", index=False, header=False, sep=',')


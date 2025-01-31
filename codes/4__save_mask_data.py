#########################################################################
# to save the usefull data into txt files                               #
#########################################################################

import numpy as np
from datetime import datetime
from matplotlib.dates import DateFormatter
import glob

# dtype for apex data and lcst
dtype1 = [('date', 'U10'), ('hour', 'U8'), ('pwv', float), ('hum', float), ('press', float), ('temp', float)]

dtype2 = [('date', 'U10'), ('hour', 'U8'), ('bcc', float), ('bba1', float), ('bba2', float), ('lux', float), ('lux_white', float), ('uva', float), ('uvb', float), ('t1', float), ('t2', float), ('t3', float), ('t4', float), ('t5', float), ('t6', float), ('t7', float), ('t8', float), ('t9', float), ('t10', float), ('t11', float), ('t12', float), ('t13', float), ('t14', float), ('t15', float), ('t16', float), ('t17', float), ('t18', float), ('t19', float), ('t20', float), ('temp', float), ('press', float), ('hum', float)]

# the folders where we have the avg and usefull data
apex_folder = "/path/to/the/avg/usefull/apex/data/"
lcst_folder = "/path/to/the/avg/usefull/lcst/data/"

apex_files = glob.glob(apex_folder + "*.txt")
lcst_files = glob.glob(lcst_folder + "*.txt")

# set an array of dates of the usefull data in format mmdd
dates = ["1017", "1019", "1020","1024", "1031", "1101","1102", "1103", "1104","1106", "1107", "1108"]

# empty arrays to be filled later
data_apex, data_lcst = [], []
apex_bcc, lcst_bcc = [], []
apex_bba, lcst_bba = [], []

# iterate over the files of each folder
for apex_file, lcst_file in zip(apex_files, lcst_files):
    apex = np.loadtxt(apex_file, delimiter=',', dtype=dtype1)
    lcst = np.loadtxt(lcst_file, delimiter=',', dtype=dtype2)
    datetime_str = [f"{date} {hour}" for date, hour in zip(lcst['date'], lcst['hour'])]
    hour_datetime = [datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') for date_str in datetime_str]
    time = np.array(hour_datetime)

    # mask1 for the bcc sensor: delete the hours when the sun passes through the 35° fov of the sensor
    mask1 = [i for i, dt in enumerate(time)
            if dt.strftime('%m%d') in dates and not (
                (dt.hour == 13 and dt.minute >=10) or
                (14 <= dt.hour <=17) or
                (dt.hour == 18 and dt.minute <30)
                )]

    # mask2 for the bba sensor: delete the hours when the sun passes through the 75° fov of the sensor
    mask2 = [i for i, dt in enumerate(time)
            if dt.strftime('%m%d') in dates and not (
                (dt.hour == 11 and dt.minute >=5) or
                (12 <= dt.hour <=21) or
                (dt.hour == 22 and dt.minute <30)
                )]

    # save the full data, with no mask applied
    data_apex.extend(apex)
    data_lcst.extend(lcst)

    # save the data with the mask applied to each sensor
    apex_bcc.extend(apex[mask1])
    apex_bba.extend(apex[mask2])
    lcst_bcc.extend(lcst[mask1])
    lcst_bba.extend(lcst[mask2])

# convert the extended data into arrays
data_apex, data_lcst = np.array(data_apex, dtype=dtype1), np.array(data_lcst, dtype=dtype2)
apex_bcc, lcst_bcc = np.array(apex_bcc), np.array(lcst_bcc)
apex_bba, lcst_bba = np.array(apex_bba), np.array(lcst_bba)

# save the data into .txt files: for the full, mask1 and mask2 data
np.savetxt('/home/usuario/Documentos/Universidad/2024/10Semestre/TesisI/apex/data_mask/data_apex.txt', data_apex, fmt='%s,%s,%.2f,%.2f,%.2f,%.2f', delimiter=',')
np.savetxt('/home/usuario/Documentos/Universidad/2024/10Semestre/TesisI/apex/data_mask/apex_bcc.txt', apex_bcc, fmt='%s,%s,%.2f,%.2f,%.2f,%.2f', delimiter=',')
np.savetxt('/home/usuario/Documentos/Universidad/2024/10Semestre/TesisI/apex/data_mask/apex_bba.txt', apex_bba, fmt='%s,%s,%.2f,%.2f,%.2f,%.2f', delimiter=',')

np.savetxt('/home/usuario/Documentos/Universidad/2024/10Semestre/TesisI/apex/data_mask/data_lcst.txt', data_lcst, fmt='%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f', delimiter=',')
np.savetxt('/home/usuario/Documentos/Universidad/2024/10Semestre/TesisI/apex/data_mask/lcst_bcc.txt', lcst_bcc, fmt='%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f', delimiter=',')
np.savetxt('/home/usuario/Documentos/Universidad/2024/10Semestre/TesisI/apex/data_mask/lcst_bba.txt', lcst_bba, fmt='%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f', delimiter=',')

#########################################################################
# to plot the lcst data, for each sensor for all days                   #
#########################################################################

import numpy as np
import matplotlib
matplotlib.use('qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime

# header of the data
dtype = [('date', 'U10'), ('hour', 'U8'),
         ('bcc', float), ('bba1', float), ('bba2', float),
         ('lux', float), ('lux_white', float),
         ('uva', float), ('uvb', float),
         ('tri1', float), ('tri2', float), ('tri3', float), ('tri4', float), ('tri5', float), ('tri6', float), ('tri7', float), ('tri8', float), ('tri9', float), ('tri10', float), ('tri11', float), ('tri12', float), ('tri13', float), ('tri14', float), ('tri15', float), ('tri16', float), ('tri17', float), ('tri18', float), ('tri19', float), ('tri20', float),
         ('temp', float), ('press', float), ('hum', float)]
#available days (actually, the average days where we have the 1440 points, i.e, a full day of data, with no-missing points)
print("Choose a day:")
print("October  : 17, 19, 20, 22, 23, 24, 26, 27, 28, 29, 31")
print("November : 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19 ,20, 21, 22, 23, 24, 26, 27, 28, 29, 30")
print("December : 11, 16, 18,20, 21, 22, 23, 24, 25")
print("January  : 02, 03, 04, 06, 07, 08, 09, 16, 17, 18, 19 ,20, 21, 22")
day = str(input("YYMMDD: "))

#read the data, and set the date time correct
data = np.loadtxt(f"/path/to/the/avg/files/20{day}.txt", delimiter=',', dtype=dtype)
datetime_str = [f"{date} {hour}" for date, hour in zip(data['date'], data['hour'])]
hour_datetime = [datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') for date_str in datetime_str]

#then we need to choose a sensor: ir for the sky temperature; uv for the uv sensors; triad for the 18 channels spectrometer; bme for the ambient sensor
print("Choose a sensor: \nir  | uv | triad | bme")
sensor = str(input())

if sensor == 'ir':
    fig, ax = plt.subplots(figsize=(16,16))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')
    ax.xaxis.set_major_formatter(date_formatter)

    ax.plot(hour_datetime, data['bcc']/100, 'b-', label='BCC')
    ax.set_xlabel("Date [UTC]")
    ax.set_ylabel("Temperature [C]")
    ax.legend()
    plt.show()
    #---------------------------------------------------------------------#
    fig, ax = plt.subplots(figsize=(16,16))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')
    ax.xaxis.set_major_formatter(date_formatter)

    ax.plot(hour_datetime, data['bba1']/100, 'b-', label='BBA1')
    ax.set_xlabel("Date [UTC]")
    ax.set_ylabel("Temperature [C]")
    ax.legend()
    plt.show()
    #---------------------------------------------------------------------#
    fig, ax = plt.subplots(figsize=(16,16))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')
    ax.xaxis.set_major_formatter(date_formatter)

    ax.plot(hour_datetime, data['bba2']/100, 'b-', label='BBA2')
    ax.set_xlabel("Date [UTC]")
    ax.set_ylabel("Temperature [C]")
    ax.legend()
    plt.show()

if sensor == 'uv':
    fig, ax = plt.subplots(figsize=(16,16))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')
    ax.xaxis.set_major_formatter(date_formatter)

    ax.plot(hour_datetime, data['uva'], 'b-', label='UV A')
    ax.set_xlabel("Date [UTC]")
    ax.set_ylabel("~[$\\mu$W/cm2]")
    ax.legend()
    plt.show()
    #---------------------------------------------------------------------#
    fig, ax = plt.subplots(figsize=(16,16))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')
    ax.xaxis.set_major_formatter(date_formatter)

    ax.plot(hour_datetime, data['uvb'], 'b-', label='UV B')
    ax.set_xlabel("Date [UTC]")
    ax.set_ylabel("~[$\\mu$W/cm2]")
    ax.legend()
    plt.show()

if sensor == 'bme':
    fig, ax = plt.subplots(figsize=(16,16))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')
    ax.xaxis.set_major_formatter(date_formatter)

    ax.plot(hour_datetime, data['temp']/100, 'b-', label='Ambient Temperature')
    ax.set_xlabel("Date [UTC]")
    ax.set_ylabel("Temperature [C]")
    ax.legend()
    plt.show()
    #---------------------------------------------------------------------#
    fig, ax = plt.subplots(figsize=(16,16))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')
    ax.xaxis.set_major_formatter(date_formatter)

    ax.plot(hour_datetime, data['hum']/100, 'b-', label='UV B')
    ax.set_xlabel("Date [UTC]")
    ax.set_ylabel("Humidity [%]")
    ax.legend()
    plt.show()
    #---------------------------------------------------------------------#
    fig, ax = plt.subplots(figsize=(16,16))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')
    ax.xaxis.set_major_formatter(date_formatter)

    ax.plot(hour_datetime, data['press'], 'b-', label='UV B')
    ax.set_xlabel("Date [UTC]")
    ax.set_ylabel("Pressure [kPa]")
    ax.legend()
    plt.show()

if sensor == 'triad':
    fig, ax = plt.subplots(2,3, figsize=(18,18))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')

    ax[0,0].xaxis.set_major_formatter(date_formatter)
    ax[0,0].plot(hour_datetime, data['tri1'], 'b-', label='A 410 nm')
    ax[0,0].set_xlabel("Date [UTC]")
    ax[0,0].set_ylabel("~[$\\mu$W/cm2]")
    ax[0,0].legend()
    ax[0,1].xaxis.set_major_formatter(date_formatter)
    ax[0,1].plot(hour_datetime, data['tri2'], 'b-', label='B 435 nm')
    ax[0,1].set_xlabel("Date [UTC]")
    ax[0,1].set_ylabel("~[$\\mu$W/cm2]")
    ax[0,1].legend()
    ax[0,2].xaxis.set_major_formatter(date_formatter)
    ax[0,2].plot(hour_datetime, data['tri3'], 'b-', label='C 460 nm')
    ax[0,2].set_xlabel("Date [UTC]")
    ax[0,2].set_ylabel("~[$\\mu$W/cm2]")
    ax[0,2].legend()
    ax[1,0].xaxis.set_major_formatter(date_formatter)
    ax[1,0].plot(hour_datetime, data['tri4'], 'b-', label='D 485 nm')
    ax[1,0].set_xlabel("Date [UTC]")
    ax[1,0].set_ylabel("~[$\\mu$W/cm2]")
    ax[1,0].legend()
    ax[1,1].xaxis.set_major_formatter(date_formatter)
    ax[1,1].plot(hour_datetime, data['tri5'], 'b-', label='E 510 nm')
    ax[1,1].set_xlabel("Date [UTC]")
    ax[1,1].set_ylabel("~[$\\mu$W/cm2]")
    ax[1,1].legend()
    ax[1,2].xaxis.set_major_formatter(date_formatter)
    ax[1,2].plot(hour_datetime, data['tri6'], 'b-', label='F 535 nm')
    ax[1,2].set_xlabel("Date [UTC]")
    ax[1,2].set_ylabel("~[$\\mu$W/cm2]")
    ax[1,2].legend()

    plt.show()
    #---------------------------------------------------------------------#
    fig, ax = plt.subplots(2,3, figsize=(18,18))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')

    ax[0,0].xaxis.set_major_formatter(date_formatter)
    ax[0,0].plot(hour_datetime, data['tri7'], 'b-', label='G 560 nm')
    ax[0,0].set_xlabel("Date [UTC]")
    ax[0,0].set_ylabel("~[$\\mu$W/cm2]")
    ax[0,0].legend()
    ax[0,1].xaxis.set_major_formatter(date_formatter)
    ax[0,1].plot(hour_datetime, data['tri8'], 'b-', label='H 585 nm')
    ax[0,1].set_xlabel("Date [UTC]")
    ax[0,1].set_ylabel("~[$\\mu$W/cm2]")
    ax[0,1].legend()
    ax[0,2].xaxis.set_major_formatter(date_formatter)
    ax[0,2].plot(hour_datetime, data['tri9'], 'b-', label='R 610 nm')
    ax[0,2].set_xlabel("Date [UTC]")
    ax[0,2].set_ylabel("~[$\\mu$W/cm2]")
    ax[0,2].legend()
    ax[1,0].xaxis.set_major_formatter(date_formatter)
    ax[1,0].plot(hour_datetime, data['tri10'], 'b-', label='I 645 nm')
    ax[1,0].set_xlabel("Date [UTC]")
    ax[1,0].set_ylabel("~[$\\mu$W/cm2]")
    ax[1,0].legend()
    ax[1,1].xaxis.set_major_formatter(date_formatter)
    ax[1,1].plot(hour_datetime, data['tri11'], 'b-', label='S 680 nm')
    ax[1,1].set_xlabel("Date [UTC]")
    ax[1,1].set_ylabel("~[$\\mu$W/cm2]")
    ax[1,1].legend()
    ax[1,2].xaxis.set_major_formatter(date_formatter)
    ax[1,2].plot(hour_datetime, data['tri12'], 'b-', label='J 705 nm')
    ax[1,2].set_xlabel("Date [UTC]")
    ax[1,2].set_ylabel("~[$\\mu$W/cm2]")
    ax[1,2].legend()

    plt.show()
    #---------------------------------------------------------------------#
    fig, ax = plt.subplots(2,3, figsize=(18,18))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')

    ax[0,0].xaxis.set_major_formatter(date_formatter)
    ax[0,0].plot(hour_datetime, data['tri13'], 'b-', label='T 730')
    ax[0,0].set_xlabel("Date [UTC]")
    ax[0,0].set_ylabel("~[$\\mu$W/cm2]")
    ax[0,0].legend()
    ax[0,1].xaxis.set_major_formatter(date_formatter)
    ax[0,1].plot(hour_datetime, data['tri14'], 'b-', label='U 760')
    ax[0,1].set_xlabel("Date [UTC]")
    ax[0,1].set_ylabel("~[$\\mu$W/cm2]")
    ax[0,1].legend()
    ax[0,2].xaxis.set_major_formatter(date_formatter)
    ax[0,2].plot(hour_datetime, data['tri15'], 'b-', label='V 810 nm')
    ax[0,2].set_xlabel("Date [UTC]")
    ax[0,2].set_ylabel("~[$\\mu$W/cm2]")
    ax[0,2].legend()
    ax[1,0].xaxis.set_major_formatter(date_formatter)
    ax[1,0].plot(hour_datetime, data['tri16'], 'b-', label='W 860 nm')
    ax[1,0].set_xlabel("Date [UTC]")
    ax[1,0].set_ylabel("~[$\\mu$W/cm2]")
    ax[1,0].legend()
    ax[1,1].xaxis.set_major_formatter(date_formatter)
    ax[1,1].plot(hour_datetime, data['tri17'], 'b-', label='K 900 nm')
    ax[1,1].set_xlabel("Date [UTC]")
    ax[1,1].set_ylabel("~[$\\mu$W/cm2]")
    ax[1,1].legend()
    ax[1,2].xaxis.set_major_formatter(date_formatter)
    ax[1,2].plot(hour_datetime, data['tri18'], 'b-', label='L 940 nm')
    ax[1,2].set_xlabel("Date [UTC]")
    ax[1,2].set_ylabel("~[$\\mu$W/cm2]")
    ax[1,2].legend()

    plt.show()
    #---------------------------------------------------------------------#
    fig, ax = plt.subplots(figsize=(18,18))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')
    ax.xaxis.set_major_formatter(date_formatter)

    ax.plot(hour_datetime, data['tri9'], '-', label='R 610')
    ax.plot(hour_datetime, data['tri11'], '-', label='S 680')
    ax.plot(hour_datetime, data['tri13'], '-', label='T 730')
    ax.plot(hour_datetime, data['tri14'], '-', label='U 760')
    ax.plot(hour_datetime, data['tri15'], '-', label='V 810')
    ax.plot(hour_datetime, data['tri16'], '-', label='W 860')
    ax.set_xlabel("Date [UTC]")
    ax.set_ylabel("~[$\\mu$W/cm2]")
    ax.set_title("AS7265 1")
    ax.legend()
    plt.show()
    #---------------------------------------------------------------------#
    fig, ax = plt.subplots(figsize=(18,18))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')
    ax.xaxis.set_major_formatter(date_formatter)

    ax.plot(hour_datetime, data['tri7'], '-', label='G 560')
    ax.plot(hour_datetime, data['tri8'], '-', label='H 585')
    ax.plot(hour_datetime, data['tri10'], '-', label='I 645')
    ax.plot(hour_datetime, data['tri12'], '-', label='J 705')
    ax.plot(hour_datetime, data['tri17'], '-', label='K 900')
    ax.plot(hour_datetime, data['tri18'], '-', label='L 940')
    ax.set_xlabel("Date [UTC]")
    ax.set_ylabel("~[$\\mu$W/cm2]")
    ax.set_title("AS7265 2")
    ax.legend()
    plt.show()
    #---------------------------------------------------------------------#
    fig, ax = plt.subplots(figsize=(18,18))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')
    ax.xaxis.set_major_formatter(date_formatter)

    ax.plot(hour_datetime, data['tri1'], '-', label='A 410')
    ax.plot(hour_datetime, data['tri2'], '-', label='B 435')
    ax.plot(hour_datetime, data['tri3'], '-', label='C 460')
    ax.plot(hour_datetime, data['tri4'], '-', label='D 485')
    ax.plot(hour_datetime, data['tri5'], '-', label='E 510')
    ax.plot(hour_datetime, data['tri6'], '-', label='F 535')
    ax.set_xlabel("Date [UTC]")
    ax.set_ylabel("~[$\\mu$W/cm2]")
    ax.set_title("AS7265 3")
    ax.legend()
    plt.show()
    #---------------------------------------------------------------------#
    fig, ax = plt.subplots(figsize=(18,18))
    date_formatter = DateFormatter('%Y-%m-%d\n%H:%M')
    ax.xaxis.set_major_formatter(date_formatter)

    ax.plot(hour_datetime, data['tri1'], '-', color='black', label='A 410')
    ax.plot(hour_datetime, data['tri2'], '-', color='magenta', label='B 435')
    ax.plot(hour_datetime, data['tri3'], '-', color='lightcoral', label='C 460')
    ax.plot(hour_datetime, data['tri4'], '-', color='maroon', label='D 485')
    ax.plot(hour_datetime, data['tri5'], '-', color='red', label='E 510')
    ax.plot(hour_datetime, data['tri6'], '-', color='sienna', label='F 535')
    ax.plot(hour_datetime, data['tri7'], '-', color='peachpuff', label='G 560')
    ax.plot(hour_datetime, data['tri8'], '-', color='darkorange', label='H 585')
    ax.plot(hour_datetime, data['tri9'], '-', color='moccasin', label='R 610')
    ax.plot(hour_datetime, data['tri10'], '-', color='gold', label='I 645')
    ax.plot(hour_datetime, data['tri11'], '-', color='darkkhaki', label='S 680')
    ax.plot(hour_datetime, data['tri12'], '-', color='lawngreen', label='J 705')
    ax.plot(hour_datetime, data['tri13'], '-', color='darkgreen', label='T 730')
    ax.plot(hour_datetime, data['tri14'], '-', color='turquoise', label='U 760')
    ax.plot(hour_datetime, data['tri15'], '-', color='aqua', label='V 810')
    ax.plot(hour_datetime, data['tri16'], '-', color='dodgerblue', label='W 860')
    ax.plot(hour_datetime, data['tri17'], '-', color='navy', label='K 900')
    ax.plot(hour_datetime, data['tri18'], '-', color='darkviolet', label='L 940')
    ax.set_xlabel("Date [UTC]")
    ax.set_ylabel("~[$\\mu$W/cm2]")
    ax.legend()
    plt.show()
else:
    print("Choose a sensor.")

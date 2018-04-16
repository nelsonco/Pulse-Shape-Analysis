import numpy as np
import os.path
import glob

########################### Input Parameters ####################################
channel_number = 2
date_list = ["2018-03-27"] # List of dates which have data files that you would like to convert
directory = "/Users/courtneynelson/Documents/Picoscope-Data/"
addDir = False # If there is a secondary folder in which the data is included specify here in str format.


########################### Bulk Code ##########################################

datadir_list=[]
datadirA_list=[]
datadirB_list=[]
data_set = []
data_setA = []
data_setB = []




for date in date_list:
    if addDir == False:
        dir = directory + date
    elif addDir != False:
        dir = directory + date + "/" + addDir

    txtdir = dir + "/txt"

    if channel_number == 1:
        if not os.path.exists(txtdir):
            os.makedirs(txtdir)
        datadir = glob.glob(dir + "/*.npy")
        for data in datadir:
            data_array = np.load(data)
            np.savetxt(txtdir, data_array)

    if channel_number == 2:
        if not os.path.exists(txtdir+"A"):
            os.makedirs(txtdir+"A")
        if not os.path.exists(txtdir+"B"):
            os.makedirs(txtdir+"B")
        datadirA = glob.glob(dir + "/A*.npy")
        datadirB = glob.glob(dir + "/B*.npy")
        for data in datadirA:
            data_array = np.load(data)
            np.savetxt(data.replace("/A","/txtA/A").replace(".npy",".txt"), data_array)
        for data in datadirB:
            data_array = np.load(data)
            np.savetxt(txtdir+"B/"+data[-20:-4]+".txt", data_array)

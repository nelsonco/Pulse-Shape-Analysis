from picoscope import ps5000a
from picoscope import picobase
import matplotlib.pyplot as plt
import numpy as np
import time
import os.path

ps = ps5000a.PS5000a(serialNumber=None, connect=True)

################## Starts up the signal generator on the Picoscope #############

#pktopk: set the peak to peak voltage in microvolts


pktopk = 20
siggen = picobase._PicoscopeBase.setSigGenBuiltInSimple(ps,offsetVoltage=0,
                                pkToPk=pktopk, waveType="Square",
                                frequency=5E2, shots=10000, triggerType="Rising",
                                triggerSource="None", stopFreq=None,
                                increment=10.0, dwellTime=1E-1, sweepType="Up",
                                numSweeps=2)

ps.setChannel(channel="A", coupling="AC", VRange=5, VOffset=5) #Trying a VOffset to increase resolution
ps.setChannel(channel="B", coupling="AC", VRange=5)
ps.setChannel(channel="C", enabled=False)
ps.setChannel(channel="D", enabled=False)



################# Adjustable Initial Conditions ################################

n_captures = 10000 # Sets the number of capture (records n trigger events)
sample_interval = 2e-9  
duration = 500e-9  # 10 ms
ps.setResolution('8')
run_time = 360

################################################################################


timebase = ps.getTimeBaseNum(sample_interval)
timestep = ps.getTimestepFromTimebase(timebase)

################################################################################

actual_interval = ps.setSamplingInterval(sample_interval, duration)
print(actual_interval)
max_samples = ps.memorySegments(n_captures)  #returns maximum number of samples
print("maximum number of samples = " + str(max_samples))
ps.setNoOfCaptures(n_captures)
dataA = np.zeros((n_captures, max_samples), dtype=np.int16)
dataB = np.zeros((n_captures, max_samples), dtype=np.int16)

##################### Initiate Trigger #########################################

ps.setSimpleTrigger("A", threshold_V=-0.1, timeout_ms=0, direction="Falling")

##################### Record Time of Data Accuisition ##########################
print("Logging Time")
t1s = time.time()
t0s = time.time() # Get the local time
t2 = 0
t3 = 0
n=0
##Trial

while (t1s - t0s)< (run_time-(t3-t2)):
    print(n)
    t1 = time.localtime() # Get the local time
    T1 = time.strftime("%Y-%m-%d-%H:%M:%S", t1) # Format the local time

##################### Run Picoscope ############################################

    t2 = time.time()
    ps.runBlock(pretrig=0.2) #pretrig is a percentage of the waveform after trigger
    ps.waitReady()

##################### Retrieve Data ############################################

    ps.getDataRawBulk(channel='A',data=dataA) #Grabs data in bits from the picoscope
    ps.getDataRawBulk(channel='B',data=dataB) #Grabs data in bits from the picoscope

    t3 = time.time()
    t4 = time.localtime()
    # dataV defines the shape of the voltage data array.
    dataVA = np.empty(np.shape(dataA), dtype=np.float64)
    dataVB = np.empty(np.shape(dataB), dtype=np.float64)

    # dataPico is the data that has been converted to volts
    dataPicoA = ps.rawToV('A', dataRaw=dataA, dataV=dataVA, dtype=np.float64)
    dataPicoB = ps.rawToV('B', dataRaw=dataB, dataV=dataVB, dtype=np.float64)

##################### Sort Data ################################################

    i = 0
    savedA = []
    savedB = []
    data_save = np.empty(np.shape(dataA),dtype=np.float64)
    while i < len(dataPicoB[:,0])-1:
        peak = dataPicoA[i,:].tolist().index(dataPicoA[i,:].min())
        peak_trig = dataPicoB[i,int(peak)]
        if abs(peak_trig)>0.5:
            savedA = np.append(savedA,dataPicoA[i,:ps.noSamples])
            savedB = np.append(savedB,dataPicoB[i,:ps.noSamples])
        i = i + 1
    savedA = np.reshape(savedA, (-1,250))
    savedB = np.reshape(savedB, (-1,250))

##################### Save Data to File ########################################
    if savedA[:,53].any() != 0:
        directory = "C:/Users/Neutrons/Documents/Picoscope5443A/python/Picoscope-Data/"+T1[:10]
        if not os.path.exists(directory):
            os.makedirs(directory)
        txt_file = time.strftime("%Y-%m-%d-%H%M%S",t1)
        t4 = time.strftime("%Y-%m-%d-%H%M%S",t4)
        infoA = os.path.join(directory, "A"+txt_file+str(t4[-7:-1]))
        x = np.arange((-0.2*duration),0.8*duration-0.5*sample_interval,(duration)/ps.noSamples)
        dataPicoA_bi = savedA
        #dataPico_txt = np.concatenate(dataPico_bi, [x], axis=0)
        dataPicoA_txt = np.append(dataPicoA_bi, [x], 0)

        np.save(infoA, dataPicoA_txt)

        infoB = os.path.join(directory, "B"+txt_file+str(t4[-7:-1]))
        x = np.arange((-0.2*duration),0.8*duration-0.5*sample_interval,(duration)/ps.noSamples)
        dataPicoB_bi = savedB
        #dataPico_txt = np.concatenate(dataPico_bi, [x], axis=0)
        dataPicoB_txt = np.append(dataPicoB_bi, [x], 0)

        np.save(infoB, dataPicoB_txt)

        print("Done saving data")
        t1s = time.time()
    n = n + 1
    print("Captured")

##################### Graph ####################################################

a = savedA[0,:]
b = savedB[0,:]


fig, ax = plt.subplots(1,1)
plt.plot()

for i, a in enumerate(savedA):
    plt.plot((np.array(x)+i*1.2*duration), a[:ps.noSamples])
for i, b in enumerate(savedB):
    plt.plot((np.array(x)+i*1.2*duration), b[:ps.noSamples])

plt.title("Picoscope measured voltage channel A")
plt.xlabel("time (s)")
plt.ylabel("voltage (V)")

plt.show()

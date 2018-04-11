from PicoPlot import plotting_functions_version3
import numpy as np
from matplotlib import pyplot as plt
import time

directory = "c:/Users/Neutrons/Documents/Picoscope5443A/python/Picoscope-Data/"
wmin = 25 #Minimum index of the window of the data
wmax = 110 #Maximum index of the window of the data
#date_list = ["2018-03-29", "2018-03-30"]
date_list = ["2018-04-06","2018-04-07"]
#date_list =  ["2018-04-02","2018-04-03"]

#date_list = [""]
duration = 500e-9 #Record the sample duration from
noSamples = 250
dt = ((duration))/noSamples # Time step for data accuision for a capture
addDir = "D-D-5keV-0.5Torr-1700V" #Name of folder where data is saved

pico = plotting_functions_version3.picoscope(channel_number=1, duration=duration, noSamples=noSamples,qwmin=50,wmax=32+50,twmin=50+15)



pico.load_data(channel_number=2,date_list=date_list, directory = directory, addDir = addDir) #data = True if you ran the data already

start_time = time.strptime("2018-04-07-211820", "%Y-%m-%d-%H%M%S")
print(start_time)

end_time = time.strptime("2018-04-09-140345", "%Y-%m-%d-%H%M%S")
print(end_time)

t1 = time.mktime(start_time)
print(t1)
t2 = time.mktime(end_time)
print(t2)
time_elapsed = t2-t1
time_elapsed = 82243


pico.Remove_outliers(channel_number=2)
pico.Remove_out_of_range(channel_number=2, v_range=5.00, rm_outliers=True)
pico.Q_tot(channel_number=2, dt=dt, directory=directory,date_list=date_list)
pico.Q_tail(channel_number=2, dt=dt, directory=directory,date_list=date_list)
# dividing_ratio, min_q_tot, and max_peak are for the absolute values of the data

pico.peak(channel_number=2)
#open(directory+date_list[0]+"/PulseShapeData.txt", 'w')
#np.savetxt(directory+date_list[0]+"/PulseShapeData.txt", pico.data, )


################ Plot Q_tot/Q_tail ################################################
i = 0
pico.fwhm = []
pico.hm_right_ind = []
pico.hm_left_ind = []
pico.hist1=[]
pico.hist2=[]
pico.hist3=[]
target_index=[]
gtarget_index=[]
pico.double_gamma_index=[]
while i <len(pico.data[:,0])-1:
    hm = abs(pico.peaks[i]/2)
    if int(pico.peaks_index[i]) == 0 or pico.data[i,int(pico.peaks_index[i])] == pico.data[i,-1]:
        fw = 0
    elif int(pico.peaks_index[i]) != 0:
        abs_data = [abs(x) for x in pico.data[i,:]]
        hm_left_ind_list=abs(abs_data[0:int(pico.peaks_index[i])]-abs(hm))
        #print(hm_left_ind_list)
        hm_left_ind=hm_left_ind_list.tolist().index(hm_left_ind_list.min())
        #print(hm_left_ind)
        hm_left = abs(pico.data[i,int(hm_left_ind)])
        
        #print(abs_data[int(pico.peaks_index[i]):-1])
        hm_right_ind_list=abs(abs_data[int(pico.peaks_index[i]):-1]-abs(hm))
        #print(hm_right_ind_list)
        hm_right_ind=hm_right_ind_list.tolist().index(hm_right_ind_list.min())
        hm_right_ind=int(hm_right_ind+int(pico.peaks_index[i]))
        #print(hm_right_ind)
        hm_right = abs(pico.data[i,int(hm_right_ind)])
        #print(hm, hm_left,hm_right)
        fw = abs(hm_right_ind-hm_left_ind)*2
    pico.hm_right_ind=np.append(pico.hm_right_ind, abs(hm_right_ind))
    pico.hm_left_ind=np.append(pico.hm_left_ind, abs(hm_left_ind))
    N = 0
    for n in range(int(pico.hm_left_ind[i])-1,int(pico.hm_right_ind[i])+1):
         if ((pico.data[i,int(n)-1]+0.01 < pico.data[i,int(n)] and pico.data[i,int(n)+1]+0.01 < pico.data[i,int(n)]) 
         or (pico.data[i,int(n)-1] > pico.data[i,int(n)]+0.01 and pico.data[i,int(n)+1] > pico.data[i,int(n)]+0.01)):
             N=N+1
    if N>2:
        pico.double_gamma_index=np.append(pico.double_gamma_index, int(i))
    if 11.996<abs(fw)<12.004:
        pico.hist1=np.append(pico.hist1,int(i))
    elif 13.996<abs(fw)<14.004:
        pico.hist2=np.append(pico.hist2,int(i))
    elif 9.996<abs(fw)<10.004:
        pico.hist3=np.append(pico.hist3,int(i))

    if 14<abs(fw)<20 and i not in pico.double_gamma_index:
        target_index=np.append(target_index,i)
    if 0<abs(fw)<11.99 and i not in pico.double_gamma_index:
        gtarget_index=np.append(gtarget_index,i)

    #if pico.data[i,0:int(hm_left_ind)].any()<hm_left-0.01 or pico.data[i,int(hm_right_ind):-1].any()<hm_right-0.01:
    pico.fwhm = np.append(pico.fwhm,fw)
    
    i = i+1
print("completed")
pico.gamma_band(channel_number=2, dt=dt, dividing_ratio = 2.3, min_q_tot=0.8e-8, max_peak=4.9, gband_index=[int(x) for x in gtarget_index])
print("completed")
pico.neutron_band(channel_number=2, dt=dt, dividing_ratio = 2.3, min_q_tot=0.8e-8, max_peak=4.9, band_index=[int(x) for x in target_index])
print("completed")
#pico.band(channel_number=2, dt=dt, dividing_ratio = 2.3, min_q_tot=0.8e-8, max_peak=4.9)

#pico.q_selection(channel_number=2, target_list=[pico.q_tot[int(x)] for x in target_index[-15:-1]], wmin=wmin, wmax=wmax, dt=dt, date_list=date_list, directory = directory, addDir = addDir, gamma_band=True)
#print("completed")
pico.qt_scatter(ax=None, band=True, gamma_band=True, q_selection = False, date_list=date_list, directory = directory, addDir = addDir, time_elapsed=time_elapsed)
#pico.pq_scatter(ax=None, band=True, date_list=date_list, directory = directory, addDir = addDir)
#pico.b_pulse(channel_number=2, match_pulse=True, date_list=date_list, directory = directory, addDir = addDir)
#pico.match_pulse(channel_number=2, date_list=date_list, directory = directory, addDir = addDir)
print(t1)
print(t2)
print(t2-t1)
"""
################ Plot Q_tot/Q_tail ################################################
fig, ax10 = plt.subplots()
i=0
ratios = []
while i < len(pico.data[:,0]) and pico.q_tail[i] !=0 and pico.peaks[i]<4.99: #658 looks interesting
    ratio = abs(pico.q_tot[i])/abs(pico.q_tail[i])
    ratios = np.append(ratios,ratio)
    i = i + 1
ax10.hist(ratios, bins=1000, range=(0, 3))
plt.show()
plt.close()

################ Plot fwhm  ###################################################
fig, ((ax12, ax13)) = plt.subplots(2,1)

(n, bins, patches) = ax12.hist(pico.fwhm, bins=10000, range=(0, 40))
print(n)
for i in n:
    if i!=0:
        x = (n.tolist().index(i))
        #print(x) 
        print(i,bins[x], patches[x])
ax13.hist((pico.hm_right_ind*2), bins=1000, range=(int((pico.hm_right_ind*2).min()), (int((pico.hm_right_ind*2).max()))))

plt.show()
plt.close()
################ Plot Outliers ################################################
"""
"""
i = 0 
n = 0
fig, outliers = plt.subplots()
outliers.set_xlabel("time (µs)")
outliers.set_ylabel("voltage (V)")
outliers.set_title("Picoscope measured voltage channel A")
while i < len(pico.data[:,0]):
    if pico.data[i,:].max()>0.06:
        outliers.plot(pico.t, pico.data[int(i)]+n)
        n = n + 1
    i = i + 1
    
plt.show()
plt.close()
"""

################## Plot band ##################################################
"""
fig, gammas = plt.subplots()
n = 0

for i in [int(x) for x in pico.double_gamma_index]:
    if n<20:
        y = pico.data[int(i),int(pico.peaks_index[int(i)])-10:int(pico.peaks_index[int(i)])+22]
        gammas.plot(pico.t[int(pico.peaks_index[int(i)])-10:int(pico.peaks_index[int(i)])+22]+n*0.1, y, linewidth=2)
        gammas.scatter(pico.t[int(pico.hm_left_ind[i])]+n*0.1,pico.data[int(i),int(pico.hm_left_ind[i])], c = "black")
        gammas.scatter(pico.t[int(pico.hm_right_ind[i])]+n*0.1,pico.data[int(i),int(pico.hm_right_ind[int(i)])], c = "black")
        n = n + 1

plt.show()
plt.close()
"""
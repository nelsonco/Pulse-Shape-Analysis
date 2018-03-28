import numpy as np
import os.path
import matplotlib.pyplot as plt
import glob
import math

######################### Set Plotting Parameters ##############################

duration = 500e-9 #Record the sample duration from
noSamples = 250
T1 = "2018-03-14" #Date of data accuisition. Data needs to be in folders with these labels
T2 = "2018-03-15"
T3 = "2018-03-14"
T4 = "2018-03-15"
# The location of the date folder that contain the data
directory = "/Users/courtneynelson/Documents/Picoscope-Data/"

wmin = 25 #Minimum index of the window of the data
wmax = 110 #Maximum index of the window of the data

channel = "A"
coupling = "AC"
VRange = "10"
Resolution = "8"
threshold_V = "-1"

################################################################################
file_list_a=[]
file_list_b=[]
files_d1_a = glob.glob(directory+T1+"/cha/*.npy") # Collects all .npy files in T1 folder
files_d2_a = glob.glob(directory+T2+"/cha/*.npy") # Collects all .npy files in T2 folder
files_d1_b = glob.glob(directory+T1+"/chb/*.npy")
files_d2_b = glob.glob(directory+T2+"/chb/*.npy")

for i in [files_d1_a,files_d2_a]:
    file_list_a=np.append(file_list_a,i)
for i in [files_d1_b,files_d2_b]:
    file_list_b=np.append(file_list_b,i)

# Creating empy sets to fill with data
q_tot_1=[] #q_tot_1 is the line integral of the curve (units: V*s)
peak=[] #peak is the minimum voltage, the peak of the pulse (units: V)
q_tail=[] #q_tail is the line integral of the curve from peak (units: V*s)
q_tot_2=[] #q_tot_2 is the line integral of the curve (units: V*s)
outlier_i=[]
outlier_a=[]
minimum_b=[]
b_i = []
b_min = []
b_tail = []
b_tot = []
b_peak=[]
match_list=[]
peak_ind=[]
band_index = []
band_a = []
match_i = []
match_a = []

for a in file_list_b:
    dat = np.load(a)
    i = 0
    while i < len(dat[:,0])-1:
        b_val = np.min(dat[i])
        minimum_b = np.append(minimum_b,b_val)
        i = i+1


"""
    for b in b_i:
        diff = abs(l - np.min(x[int(b)]))
        diff[int(b)] = 1
        c = diff.tolist()
        match = c.index(np.min(diff))
        match_list = np.append(match_list, match)
"""
timeout = 0

for a in file_list_a:
    x = np.load(a)
    dt = ((duration))/noSamples # Time step for data accuision for a capture

    i = 0
    w=[]
    l=[]
    tail=[]
    tot=[]

    while i < len(x[:,0])-1:
        k = np.min(x[i])
        z = np.sum(x[i,wmin:wmax])
        w = np.append(w,z)
        l = np.append(l,k)
        #if 3.3<abs(k)<3.4:
            #print("i = "+str(i))
            #print("a = "+str(a))

            #if 6e-8<(abs(z)*dt)<8e-8:
                #print("This is the target : i = " + str(i))
                #print("a = "+str(a))
        i = i+1
    q_tot_1 = np.append(q_tot_1,w*dt)
    peak = np.append(peak,l)
    infot = a.replace("npy","txt")
    np.savetxt(infot, np.c_[w,l],  header="")

    i = 0

    while i < len(x[:,0])-1:
        c = x[i].tolist()
        k = c.index(x[i].min())
        peak_ind = np.append(peak_ind,k)
        p = np.sum(x[i,k+10:k+110])
        d = np.sum(x[i,k-5:k+110])
        tail = np.append(tail,p)
        tot= np.append(tot,d)
        if abs(d*dt)<1.4e-08:
            print("outlier")
            outlier_i = np.append(outlier_i,int(i))
            outlier_a = np.append(outlier_a,a)
        if 1.362<abs(x[i].min())<1.37 and timeout<11:
            match_i = np.append(match_i,int(i))
            match_a = np.append(match_a,a)
            timeout = timeout+1
        if 3.6<abs(x[i].min())<3.8 and 11<timeout<21:
            print("match")
            match_i = np.append(match_i,int(i))
            match_a = np.append(match_a,a)
            timeout = timeout+1
        if abs(d/p) < 3.7 and 1.84e-08<abs(d*dt)<1.05e-07 and abs(x[i,k+20:k+110]).max()< 0.23:
            band_index = np.append(band_index, i)
            band_a = np.append(band_a,a)
        i = i+1
    q_tail = np.append(q_tail,tail*dt)
    q_tot_2 = np.append(q_tot_2,tot*dt)


match_i = match_i[0:21]
match_a = match_a[0:21]

for a in file_list_b:
    i = 0
    dat = np.load(a)
    while i < len(dat[:,0]-1):
        k = peak_ind[i]
        if abs(dat[i,int(k)])>0.5:
            b_tail = np.append(b_tail,tail[int(i)])
            b_tot = np.append(b_tot,tot[int(i)])
            b_peak = np.append(b_peak,peak[int(i)])
        i = i +1
    b_tail = b_tail*dt
    b_tot = b_tot*dt

q_tot_band = []
q_tail_band = []

i = 0
while i < len(q_tail)-1:
    if abs(q_tot_2[i]/q_tail[i]) < 3.7 and 1.84e-08<abs(q_tot_2[i])<1.05e-07:
        q_tot_band = np.append(q_tot_band, q_tot_2[i])
        q_tail_band = np.append(q_tail_band, q_tail[i])
    i = i + 1

fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.scatter(abs(q_tot_1),abs(peak), c="blue", marker=".", s=1**2)
ax1.scatter(abs(b_tot),abs(b_peak), marker="+", s=4**2, c="red")
ax1.set_xlim(0,30e-08)
ax1.set_ylim(1,8)
ax1.set_xlabel("Q_tot (V*t)")
ax1.set_ylabel("Peak (V)")
ax1.set_title("Integral under the curve vs Peak")

ax2.scatter(abs(q_tail),abs(q_tot_2), marker=".", s=1**2)
ax2.scatter(abs(b_tail),abs(b_tot), marker="+", s=4**2, c="red")
ax2.scatter(abs(q_tail_band),abs(q_tot_band), marker="+",s=4**2, c="orange")

ax2.set_xlim(0,30e-08)
ax2.set_ylim(0,30e-08)
ax2.set_xlabel("Q_tail (V*t)")
ax2.set_ylabel("Q_tot (V*t)")
ax2.set_title("Integral under the curve vs Integral tail")

plt.savefig("Trends" + ".png")

plt.show()



fig, ax4 = plt.subplots(1, 1)

ax4.scatter(abs(peak), abs(minimum_b), marker=".")
ax4.set_xlim(0,10)
ax4.set_ylim(0,1)
ax4.set_xlabel("Peak A")
ax4.set_ylabel("Minimum B")
ax4.set_title("Picoscope measured voltage channel A with Bs")

plt.savefig("Comparison" + ".png")

plt.show()

"""
fig, ax3 = plt.subplots(1, 1)

n=0.5
for m in match_list:
    ax3_x = np.arange((-0.2*duration) + n*duration,0.8*duration-1e-9 + n*duration,(duration)/noSamples)*1e6
    ax3.plot(ax3_x[wmin:wmax], x[int(m),wmin:wmax], ls="--", c="orange")
    n = n+1
"""

"""
file_nm = T2+"/"+"A2018-03-12-132224"
info = os.path.join(directory, file_nm+".npy")
dat = np.load(info)
ax3_x = np.arange((-0.2*duration),0.8*duration-1e-9,(duration)/noSamples)*1e6
ax3_x = ax3_x[wmin:wmax]
ax3_y = dat[70,wmin:wmax]
"""
"""
ax3.set_xlim(-0.2*duration*1e6-0.2*duration*1e6, duration*1e6+0.2*duration*1e6)
ax3.set_ylim(-4,0.1)
ax3.set_xlabel("time (µs)")
ax3.set_ylabel("voltage (V)")
ax3.set_title("Picoscope measured voltage channel A")

plt.show()
"""

fig, ax5 = plt.subplots(1, 1)
data=[]
n = 0
for j in outlier_a:
    dat = np.load(j)
    i = outlier_a.tolist().index(j)
    i = outlier_i[i]
    ax5_x = np.arange((-0.2*duration)+(n*0.5*duration),0.8*duration-1e-9+(n*0.5*duration),(duration)/noSamples)*1e6
    ax5.plot(ax5_x[wmin:wmax], dat[int(i),wmin:wmax])
    n=n+1

"""
file_nm = T2+"/"+"A2018-03-12-132224"
info = os.path.join(directory, file_nm+".npy")
dat = np.load(info)
ax3_x = np.arange((-0.2*duration),0.8*duration-1e-9,(duration)/noSamples)*1e6
ax3_x = ax3_x[wmin:wmax]
ax3_y = dat[70,wmin:wmax]
"""

ax5.set_xlim(-0.2*duration*1e6-0.2*duration*1e6, duration*1e6+0.2*duration*1e6)
ax5.set_ylim(-4,0.1)
ax5.set_xlabel("time (µs)")
ax5.set_ylabel("voltage (V)")
ax5.set_title("Picoscope measured voltage channel A")

plt.show()

fig, ax6 = plt.subplots(1, 1)
data=[]
n = 0
for j in band_a:
    dat = np.load(j)
    w = j.replace("cha","chb")
    w = w.replace("A","B")
    x = np.load(w)
    i = band_a.tolist().index(j)
    i = band_index[int(i)]
    k = dat[int(i)].tolist().index(dat[int(i)].min())
    print(dat[int(i)].min())
    ax6_x = np.arange((-0.2*duration)+(n*0.5*duration),0.8*duration-1e-9+(n*0.5*duration),(duration)/noSamples)*1e6
    ax6.plot(ax6_x[int(k)-20:110], dat[int(i),int(k)-20:110], c = "black")
    ax6.plot(ax6_x[int(k)-20:110], x[int(i),int(k)-20:110])
    n=n+1

index = 0
for j in match_a:
    dat = np.load(j)
    #i = match_a.tolist().index(j)
    l = int(index/10)
    i = match_i[int(index)]
    k = dat[int(i)].tolist().index(dat[int(i)].min())
    ax6_x = np.arange((-0.2*duration)+l*6*0.5*duration,0.8*duration-1e-9+(l*6*0.5*duration),(duration)/noSamples)*1e6
    ax6.plot(ax6_x[int(k)-20:110], dat[int(i),int(k)-20:110])
    index = index + 1

"""
file_nm = T2+"/"+"A2018-03-12-132224"
info = os.path.join(directory, file_nm+".npy")
dat = np.load(info)
ax3_x = np.arange((-0.2*duration),0.8*duration-1e-9,(duration)/noSamples)*1e6
ax3_x = ax3_x[wmin:wmax]
ax3_y = dat[70,wmin:wmax]
"""

ax6.set_xlim(-0.2*duration*1e6-0.2*duration*1e6, duration*1e6+0.2*duration*1e6)
ax6.set_ylim(-4,0.1)
ax6.set_xlabel("time (µs)")
ax6.set_ylabel("voltage (V)")
ax6.set_title("Picoscope measured voltage channel A")

plt.show()

plt.close()

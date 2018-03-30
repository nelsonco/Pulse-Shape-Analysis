import numpy as np
import os.path
from matplotlib import pyplot as plt
import glob
import math


class picoscope:

    def __init__(self,channel_number, duration, noSamples):
            self.channel_number=channel_number
            self.t = np.arange((-0.2*duration)+(0.5*duration),0.8*duration-1e-9+(0.5*duration),(duration)/noSamples)*1e6
            self.duration = duration
            self.noSamples = noSamples


    def load_data(self, channel_number,date_list, directory, addDir = False):
            self.datadir_list=[]
            self.datadirA_list=[]
            self.datadirB_list=[]
            self.data_set = []
            self.data_setA = []
            self.data_setB = []
            for date in date_list:
                if channel_number == 1:
                    if addDir == False:
                        datadir = glob.glob(directory+date+"/*.npy")
                    elif addDir != False:
                        datadir = glob.glob(directory+date+"/"+addDir+"/*.npy")
                    self.datadir_list = np.append(self.datadir_list, datadir)
                if channel_number == 2:
                    if addDir == False:
                        self.datadirA = glob.glob(directory+date+"/A*.npy")
                        self.datadirB = glob.glob(directory+date+"/B*.npy")
                    elif addDir != False:
                        self.datadirA = glob.glob(directory+date+"/"+addDir+"/A*.npy")
                        self.datadirB = glob.glob(directory+date+"/"+addDir+"/B*.npy")
                    self.datadirA_list = np.append(self.datadirA_list, self.datadirA)
                    self.datadirB_list = np.append(self.datadirB_list, self.datadirB)
            for data in self.datadir_list:
                if data == self.datadir_list[0]:
                    self.data_set = np.load(data)
                elif data != self.datadir_list[0]:
                    self.data = np.load(data)
                    self.data_set = np.append(self.data_set,self.data[0:-1,:], axis=0)
            for data in self.datadirA_list:
                self.dataA = np.load(data)
                self.data_setA = np.append(self.data_setA,self.dataA[0:-1,:])
                self.data_setA = np.reshape(self.data_setA, (-1,int(self.noSamples)))
            for data in self.datadirB_list:
                self.dataB = np.load(data)
                self.data_setB = np.append(self.data_setB,self.dataB[0:-1,:])
                self.data_setA = np.reshape(self.data_setA, (-1,int(self.noSamples)))

    def Q_tail(self, channel_number, wmin, wmax, dt, directory,date_list):
        #From full width half max point after peak to where tail rises to zero
            if channel_number == 1:
                self.data = self.data_set
            elif channel_number == 2:
                self.data = self.data_setA

            a = 0
            self.q_tail = []
            while a < len(self.data[:,0]):
                self.data_list = self.data[a].tolist()
                self.peak_index = self.data_list.index(self.data[a].min())
                tsum = np.sum(self.data[a,int(self.peak_index)+4:int(self.peak_index)+22])

                #if abs(self.data[a].min()) < 9.99:
                self.q_tail = np.append(self.q_tail,tsum*dt)
                a =a + 1
            print("q_tail = ", self.q_tail)

    def Q_tot(self,channel_number, wmin, wmax, dt, date_list, directory):
            if channel_number == 1:
                self.data = self.data_set
            elif channel_number == 2:
                self.data = self.data_setA
            i = 0
            self.q_tot = []
            self.q_tot_index = []
            while i < len(self.data[:,0]):
                data_list = self.data[i].tolist()
                peak_index = data_list.index(self.data[i].min())
                #if abs(self.data[i].min()) < 9.99:
                qsum = np.sum(self.data[i, int(peak_index)-10:int(peak_index)+22])
                self.q_tot = np.append(self.q_tot,qsum*dt)
                self.q_tot_index = np.append(self.q_tot_index, i)
                i = i + 1
            print("q_tot = ", self.q_tot)
    def peak(self,channel_number):
        if channel_number == 1:
            self.data = self.data_set
        elif channel_number == 2:
            self.data = self.data_setA
        self.peaks = []
        self.peaks_index = []
        i = 0
        while i < len(self.data[:,0]):
            k = np.min(self.data[i])
            l = self.data[i].tolist().index(k)
            #if abs(self.data[i].min()) < 9.99:
            self.peaks = np.append(self.peaks,k)
            self.peaks_index = np.append(self.peaks_index, l)
            i = i + 1
    def band(self, channel_number, dt, dividing_ratio, min_q_tot, max_peak, band_index=[]):
            if channel_number == 1:
                self.data = self.data_set
            elif channel_number == 2:
                self.data = self.data_setA
            if band_index != []:
                self.b_peaks = []
                self.bq_tot = []
                self.bq_tail = []
                self.b_peaks_index = []
                self.band_index = band_index
                for i in self.band_index:
                     self.bq_tot = np.append(self.bq_tot, self.q_tot[i])
                     self.bq_tail = np.append(self.bq_tail, self.q_tail[i])
                     self.b_peaks = np.append(self.b_peaks, self.peaks[i])
                     self.b_peaks_index = np.append(self.b_peaks_index, self.peaks_index[i])

            if band_index == []:
                self.b_peaks = []
                i = 0
                self.band_index = []
                self.bq_tot = []
                self.bq_tail = []
                self.b_peaks_index = []
                while i < len(self.q_tot):
                    if abs(self.q_tot[i]/self.q_tail[i]) < dividing_ratio and abs(self.q_tot[i])>min_q_tot and abs(self.data[i].min()) < max_peak:
                        print(abs(self.q_tot[i]/self.q_tail[i]))
                        self.bq_tot = np.append(self.bq_tot, self.q_tot[i])
                        self.bq_tail = np.append(self.bq_tail, self.q_tail[i])
                        self.band_index = np.append(self.band_index, i)
                        k = np.min(self.data[i])
                        k_index = self.data[i].tolist().index(k)
                        self.b_peaks = np.append(self.b_peaks, k)
                        self.b_peaks_index = np.append(self.b_peaks_index, k_index)
                    i = i + 1

    def q_selection(self, channel_number, target_list, wmin, wmax, dt, date_list, directory, addDir = False):
            if channel_number == 1:
                self.data = self.data_set
            elif channel_number == 2:
                self.data = self.data_setA
            fig, self.ax7 = plt.subplots()
            self.ax7.set_xlabel("time (µs)")
            self.ax7.set_ylabel("voltage (V)")
            self.ax7.set_title("Picoscope measured voltage channel A")
            l = 0
            for target in target_list:
                self.diff_set = []
                for bq_tot in self.bq_tot:
                    self.diff = abs(abs(bq_tot)-abs(target))
                    self.diff_set = np.append(self.diff_set, self.diff)
                self.target_b = self.diff_set.min()
                self.diff_list = self.diff_set.tolist()
                self.target_index = self.diff_list.index(self.target_b)
                self.target_q_tot = abs(self.bq_tot[self.target_index])
                self.i = self.band_index[int(self.target_index)]
                #i = self.q_tot_index[int(i)]
                self.y = self.data[int(self.i),int(self.peaks_index[int(self.i)])-10:int(self.peaks_index[int(self.i)])+22]
                print("target q_tot", self.target_q_tot)
    
                self.ax7.axvline(x=(self.t[int(self.peaks_index[int(self.i)])]))
                self.ax7.plot(self.t[int(self.peaks_index[int(self.i)])-10:int(self.peaks_index[int(self.i)])+22],self.y+(l*5), c = "black", linewidth=4)
                self.ax7.fill(self.t[int(self.peaks_index[int(self.i)])-10:int(self.peaks_index[int(self.i)])+22], self.y+(l*5), 'b', alpha=0.3)
             
                x = 0
                i = 0
                band_index = [int(x) for x in self.band_index]
                while i < len(self.data[:,0])-1 and x<11:
                    if abs(abs(self.target_q_tot)-abs(self.q_tot[i]))<0.01e-8 and abs(self.data[i].min()) < 4.99 and i not in band_index:
                        self.z = self.data[int(i),int(self.peaks_index[int(i)])-10:int(self.peaks_index[int(i)])+22]
                        self.ax7.plot(self.t[int(self.peaks_index[int(self.i)])-10:int(self.peaks_index[int(self.i)])+22], self.z+(l*5), '--', linewidth=2)
                        self.ax7.fill(self.t[int(self.peaks_index[int(self.i)])-10:int(self.peaks_index[int(self.i)])+22], self.z+(l*5), 'r', alpha=0.1)
                        print("q_tot = ", self.q_tot[i])
                        x = x + 1
                        print("i = ",i)
                    i = i + 1
                l = l+1
            if addDir == False:
                plt.savefig(date_list[0]+"/"+date_list[-1]+"_selection_scatter.png")
            if addDir != False:
                plt.savefig(date_list[0]+"/"+addDir+"/"+date_list[-1]+"_selection_scatter.png")
            plt.show()
   

    def qt_scatter(self, band, q_selection, date_list, directory, ax=None, addDir = False):

        if ax is None:
            fig, ax1 = plt.subplots()

            # times = [time.strptime(self.date + '-' + str(int(t)),
            #                       "%Y-%m-%d-%H%M%S")
            #         for t in self.data_dict['time']]
            ax1.scatter(abs(self.q_tail), abs(self.q_tot), marker=".", s=2**2, c = "blue")
            ax1.set_xlabel("Q_tail")
            ax1.set_ylabel("Q_total")
            ax1.set_xlim(0,30e-08)
            ax1.set_ylim(0,30e-08)
            ax1.set_title("Integral under the curve vs Integral tail")

        else:
            ax.scatter(abs(self.q_tail), abs(self.q_tot), marker=".", s=2**2, c = "blue")
            ax.set_xlabel("Q_tail")
            ax.set_ylabel("Q_total")

        if band == True:
            i = 0
            while i < len(self.band_index):
                ax1.scatter(abs(self.bq_tail[int(i)]), abs(self.bq_tot[int(i)]), marker=".", s=2**2,c='orange')
                i = i + 1
        if q_selection == True:
            ax1.scatter(abs(self.target_q_tot), abs(self.q_tail[int(self.band_index[int(self.target_index)])]), marker="+", s=2**2,c='black')

        if addDir == False:
            plt.savefig(date_list[0]+"/"+date_list[-1]+"_qt_scatter.png")
        if addDir != False:
            plt.savefig(date_list[0]+"/"+addDir+"/"+date_list[-1]+"_qt_scatter.png")

        plt.show()

        plt.close()


    def pq_scatter(self, band, date_list, directory, ax=None, addDir = False):
            if ax is None:
                fig, ax2 = plt.subplots()

                # times = [time.strptime(self.date + '-' + str(int(t)),
                #                       "%Y-%m-%d-%H%M%S")
                #         for t in self.data_dict['time']]
                ax2.scatter(abs(self.q_tot), abs(self.peaks), marker=".", s=1**2)
                ax2.set_xlabel("Q_tot")
                ax2.set_ylabel("Peak (V)")
                ax2.set_xlim(0,30e-08)
                ax2.set_ylim(1,8)
                ax2.set_title("Integral under the curve vs Peak")

            else:
                ax.scatter(abs(self.q_tot), abs(self.peaks), marker=".")
                ax.set_xlabel("Q_tot")
                ax.set_ylabel("Peak (V)")

            if band == True:
                for i in self.band_index:
                    ax2.scatter(abs(self.q_tot[int(i)]), abs(self.peaks[int(i)]), marker=".", c='orange')

            if addDir == False:
                plt.savefig(date_list[0]+"/"+date_list[-1]+"_pq_scatter.png")
            if addDir != False:
                plt.savefig(date_list[0]+"/"+addDir+"/"+date_list[-1]+"_pq_scatter.png")

            plt.show()
            plt.close()

    def b_pulse(self, channel_number, match_pulse, date_list, directory, addDir = False):
            if channel_number == 1:
                self.data = self.data_set
            elif channel_number == 2:
                self.data = self.data_setA

            n = 0

            fig, self.ax6 = plt.subplots(1, 1)
            for i in self.band_index:
                if i < 3:
                    band_list = self.band_index.tolist()
                    band_ind = band_list.index(i)
                    peak = self.data[int(i),:].tolist().index(self.data[int(i),:].min())
                    self.x = self.t[14:83]+n*self.duration
                    self.y = self.data[int(i),14:83] #83
                    print(self.y)
                    self.ax6.plot(self.x, self.y, c = "black", linewidth=3)
                    n = n + 1

            self.ax6.set_xlim(self.t.min(),n*self.t.max())
            self.ax6.set_ylim(-4,0.1)
            self.ax6.set_xlabel("time (µs)")
            self.ax6.set_ylabel("voltage (V)")
            self.ax6.set_title("Picoscope measured voltage channel A")

            if match_pulse == False:

                if addDir == False:
                    plt.savefig(date_list[0]+"/"+date_list[-1]+"_pulse_scatter.png")
                if addDir != False:
                    plt.savefig(date_list[0]+"/"+addDir+"/"+date_list[-1]+"_pulse_scatter.png")

                plt.show()

    def match_pulse(self, channel_number, date_list, directory, addDir = False):
            if channel_number == 1:
                self.data = self.data_set
            elif channel_number == 2:
                self.data = self.data_setA

            n = 0
            for b_peak in self.b_peaks:
                if n<3:
                    i = 0
                    x = 0
                    band_index = [int(x) for x in self.band_index]
                    while i < len(self.q_tot)-1 and x < 11:
                        if abs(abs(self.peaks[i])-abs(b_peak))<0.01 and i not in band_index:
                            peak = self.data[int(i),:].tolist().index(self.data[int(i),:].min())
                            self.x = self.t[14:83]+n*1.5*self.duration
                            self.y = self.data[int(i),14:83]
                            self.ax6.plot(self.x, self.y, '--', linewidth=2)
                            print("good")
                            x = x + 1
                        i = i + 1
                    n = n+1


            if addDir == False:
                plt.savefig(date_list[0]+"/"+date_list[-1]+"_pulse_scatter.png")
            if addDir != False:
                plt.savefig(date_list[0]+"/"+addDir+"/"+date_list[-1]+"_pulse_scatter.png")


            plt.show()

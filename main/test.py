from PicoPlot import plotting_functions
import numpy as np

directory = "c:/Users/Neutrons/Documents/Picoscope5443A/python/Picoscope-Data/"
wmin = 25 #Minimum index of the window of the data
wmax = 110 #Maximum index of the window of the data
date_list = ["2018-03-28"]
duration = 500e-9 #Record the sample duration from
noSamples = 250
dt = ((duration))/noSamples # Time step for data accuision for a capture
addDir = False

pico = plotting_functions.picoscope(channel_number=1, duration=duration, noSamples=noSamples)

pico.load_data(channel_number=2,date_list=date_list, directory = directory, addDir = addDir)
pico.Q_tot(channel_number=2, wmin=0, wmax=100, dt=dt, directory=directory,date_list=date_list)
pico.Q_tail(channel_number=2, wmin=0, wmax=100, dt=dt, directory=directory,date_list=date_list)
pico.band(channel_number=2, dt=dt)
pico.peak(channel_number=2)
#open(directory+date_list[0]+"/PulseShapeData.txt", 'w')
#np.savetxt(directory+date_list[0]+"/PulseShapeData.txt", pico.data, )


print('Q_tot', pico.q_tot)

pico.q_selection(channel_number=2, target=0.28e-7, wmin=wmin, wmax=wmax, dt=dt, date_list=date_list, directory = directory, addDir = addDir)
pico.qt_scatter(ax=None, band=True, q_selection = True, date_list=date_list, directory = directory, addDir = addDir)
pico.pq_scatter(ax=None, band=True, date_list=date_list, directory = directory, addDir = addDir)
pico.b_pulse(channel_number=2, match_pulse=True, date_list=date_list, directory = directory, addDir = addDir)
pico.match_pulse(channel_number=2, date_list=date_list, directory = directory, addDir = addDir)

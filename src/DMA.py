import datetime
import time
import numpy as np
import threading

from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.ticker as ptick

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

import nidaqmx
import CPC
import HV

bgColor="blue"
cColor="white"

# Format of the figues
def pltNormal():
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['figure.subplot.bottom'] = 0.15
    plt.rcParams['figure.subplot.left'] = 0.15
    plt.rcParams["font.size"]=12

# Format of the figures
def axNormal(ax):
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')
    ax.tick_params(axis='x')
    ax.tick_params(axis='y')

class DMAscan:
    def __init__(self,entriesDAQ,entriesScan,entriesHV,entriesFileName):
        self.setVal(entriesDAQ,entriesScan,entriesHV,entriesFileName)

    def setVal(self,entriesDAQ,entriesScan,entriesHV,entriesFileName):
        self.hv=HV.HV(entriesDAQ,entriesHV)
        self.cpc=CPC.CPC(entriesDAQ,entriesScan,entriesHV)
        self.Vmin=float(entriesScan[0].get())
        self.Vmax=float(entriesScan[1].get())
        self.Vstep=int(entriesScan[3].get())
        self.delayTime=float(entriesScan[4].get())
        self.HVmode=int(entriesScan[5].get())
        self.Cs=[]
        self.Vs=[]
        self.updateFlag=1
        self.stop=0
        self.fileName=entriesFileName.get()

    def figUpdate(self,window):
        pltNormal()
        frameFig=tk.LabelFrame(window,background=bgColor,bd=0)
        frameFig.place(x=430,y=10,width=550,height=520)
        fig = Figure(figsize=(6, 6), dpi=100)   #Figure
        ax = fig.add_subplot(1, 1, 1)           #Axes
        axNormal(ax)
        ax.set_xlabel("Voltage [V]")
        ax.set_ylabel(r"Concentration [cc$^{-1}$]")
        ax.scatter(self.Vs,self.Cs,color="blue")
        plt.tight_layout()
        ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        canvas = FigureCanvasTkAgg(fig, frameFig)
        canvas.get_tk_widget().pack()

    def scan(self):
    #    plt.figure(figsize=(4,4))
        for V in np.linspace(float(self.Vmin),float(self.Vmax),int(self.Vstep)):
            time.sleep(self.delayTime)
            self.hv.HVout(V)
            self.Cs=np.append(self.Cs,self.cpc.getC())
            self.Vs=np.append(self.Vs,V)
            self.updateFlag=1
            if(self.stop==1):
                break
        f=open(self.fileName,"w")
        f.write("Voltage [V],Concentration [1/cc]\n")
        for i in np.arange(np.size(self.Cs)):
            f.write(str(self.Vs[i])+","+str(self.Cs[i])+"\n")
        f.close()
        self.hv.HVout(0)

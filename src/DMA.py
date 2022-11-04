import datetime
import time
import numpy as np
import threading
from scipy.optimize import minimize

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
    def __init__(self,entriesDAQ,entriesScan,entriesHV,entriesFileName,entriesDMA):
        self.setVal(entriesDAQ,entriesScan,entriesHV,entriesFileName,entriesDMA)
        self.xflag=0

    def VtoDp(self,x):
        self.Zp=self.coeff/x
        result=minimize(self.dZp,6e-8,method="Nelder-Mead")
        return result.x[0]

    def oneone(self,x):
        return x

    def DptoZp(self,dp):
        ramda=67.0e-9
        ap=dp/2.0
        Cc=1+ramda/ap*(1.257+0.4*np.exp(-1.1*ap/ramda))
        myu=1.822e-5
        return Cc*1.6e-19/(3*np.pi*myu*dp)

    def dZp(self,dp):
        Zp2=self.DptoZp(dp)
        return ((Zp2-self.Zp)*1e10)**2

    def setVal(self,entriesDAQ,entriesScan,entriesHV,entriesFileName,entriesDMA):
        self.hv=HV.HV(entriesDAQ,entriesHV)
        self.cpc=CPC.CPC(entriesDAQ,entriesScan,entriesHV)
        self.Vmin=float(entriesScan[0].get())
        self.Vmax=float(entriesScan[1].get())
        self.Vstep=int(entriesScan[3].get())
        self.delayTime=float(entriesScan[4].get())
        self.HVmode=int(entriesScan[5].get())
        Rratio=float(entriesDMA[1].get())/float(entriesDMA[2].get())
        L=float(entriesDMA[0].get())*1e-3
        Q=(float(entriesDMA[3].get())+float(entriesDMA[4].get()))/6e4
        self.coeff=Q*np.log(Rratio)/(2.0*np.pi*L)
        self.Cs, self.Vs, self.Dps, self.Zps = [], [], [], []
        self.updateFlag=1
        self.stop=0
        self.fileName=entriesFileName.get()

    def figUpdate(self,window):
        pltNormal()
        frameFig=tk.LabelFrame(window,background=bgColor,bd=0)
        frameFig.place(x=430,y=30,width=520,height=520)
        fig = Figure(figsize=(6, 6), dpi=100)   #Figure
        ax = fig.add_subplot(1, 1, 1)           #Axes
        axNormal(ax)
        if(self.xflag==0):
            ax.set_xlabel("Voltage [V]")
            ax.scatter(self.Vs,self.Cs,color="blue")
        if(self.xflag==1):
            ax.set_xlabel("Particle diameter [nm]")
            ax.scatter(self.Dps*1e9,self.Cs,color="blue")
        if(self.xflag==2):
            ax.set_xlabel(r"Electrical mobility [cm$^2$ s$^{-1}$]")
            ax.scatter(self.Zps,self.Cs,color="blue")
        ax.set_ylabel(r"Concentration [cc$^{-1}$]")
        plt.tight_layout()
        ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        canvas = FigureCanvasTkAgg(fig, frameFig)
        canvas.get_tk_widget().pack()
        #print(dpmin)
        #secax.set_xlim(dpmin,dpmax)

    def scan(self):
    #    plt.figure(figsize=(4,4))
        self.cpc.timeOpt()
        self.cpc.timeOpt()
        for V in np.linspace(float(self.Vmin),float(self.Vmax),int(self.Vstep)):
            time.sleep(self.delayTime)
            self.hv.HVout(V)
            self.Cs=np.append(self.Cs,self.cpc.getC())
            self.Vs=np.append(self.Vs,V)
            self.Dps=np.append(self.Dps,self.VtoDp(V))
            self.Zps=np.append(self.Zps,self.Zp)
            self.updateFlag=1
            if(self.stop==1):
                break
        f=open(self.fileName,"w")
        f.write("V [V],Zp [cm2/s],Dp [nm],Conc. [1/cc]\n")
        for i in np.arange(np.size(self.Cs)):
            f.write(str(self.Vs[i])+","+str(self.Zps[i])+","+str(self.Dps[i])+","+str(self.Cs[i])+"\n")
        f.close()
        self.hv.HVout(0)

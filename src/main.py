import numpy as np
import threading

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

import nidaqmx
import CPC
import HV
import DMA

bgColor="blue"
cColor="white"

def save_data(tydata,outpath,filename):
    save_file_name =  outpath+"/"+filename
    np.savetxt(save_file_name, tydata, delimiter=',')

def main():
    window = tk.Tk()
    window.title("DMA scan test")
    window.geometry("1000x590")
    window.configure(bg=bgColor)

    # Frame setting
    frameDAQ=tk.LabelFrame(window,text="DAQ settings",font=("",15),background=bgColor,foreground="white")
    frameScan=tk.LabelFrame(window,text="Scan mode",font=("",15),background=bgColor,foreground="white")
    frameHV=tk.LabelFrame(window,text="HV parameters",font=("",15),background=bgColor,foreground="white")
    frameFile=tk.LabelFrame(window,text="File setting",font=("",15),background=bgColor,foreground="white")
    frameFix=tk.LabelFrame(window,text="Fixed mode",font=("",15),background=bgColor,foreground="white")
    frameDMA=tk.LabelFrame(window,text="DMA parameters",font=("",15),background=bgColor,foreground="white")

    # Location of the frames
    frameDAQ.place(x=10,y=10,width=195,height=200)
    frameScan.place(x=220,y=10,width=195,height=305)
    frameHV.place(x=10,y=215,width=195,height=100)
    frameFile.place(x=10,y=490,width=405,height=70)
    frameFix.place(x=220,y=320,width=195,height=170)
    frameDMA.place(x=10,y=320,width=195,height=170)

    # Labels for variables
    labelsDAQ=np.array(["CPC connection","V_CPC min","V_CPC max","HV connection","V_HV min","V_HV max"])
    labelsScan=np.array(["Min voltage","Max voltage","Time per a bin","Number of bins","Delay time","HV mode","CPC mode"])
    labelsHV=np.array(["      Slope      ","Bias"])
    labelsFix=np.array(["      Voltage      ","CPC mode"])
    labelsDMA=np.array(["Lenght","Inner diameter","Outer diameter","Sheath flow","Aerosol flow"])

    # Units of variables
    unitsDAQ=np.array([" ","V","V"," ","V","V"])
    unitsScan=np.array(["V","V","s"," ","s"," "," "])
    unitsHV=np.array([" ","V"])
    unitsFix=np.array(["V"," "])
    unitsDMA=np.array(["mm","mm","mm","L/min","L/min"])

    # Initial values
    initialsDAQ=np.array(["Dev1/ai0",0,10,"Dev1/ao1",0,5])
    initialsScan=np.array([10,1000,5,10,2,0,-1])
    initialsHV=np.array([2000,0])
    initialsFix=np.array([10,-1])
    initialsDMA=np.array([10,10,20,15,1.5])

    # Initialize entries
    entriesDAQ=[]
    entriesScan=[]
    entriesHV=[]
    entriesFix=[]
    entriesDMA=[]

    # Arrange labels, entries, and units in frames
    for i in np.arange(np.size(labelsDAQ)):
        label = tk.Label(frameDAQ,text=labelsDAQ[i],background=bgColor,foreground=cColor)
        label.grid(row=[i],column=0)
        entriesDAQ=np.append(entriesDAQ,tk.Entry(frameDAQ,width=10))
        entriesDAQ[i].grid(row=[i],column=1,sticky=tk.EW)
        entriesDAQ[i].delete(0,tk.END)
        entriesDAQ[i].insert(tk.END,initialsDAQ[i])
        label = tk.Label(frameDAQ,text=unitsDAQ[i],background=bgColor,foreground=cColor)
        label.grid(row=[i],column=2)
    for i in np.arange(np.size(labelsScan)):
        label = tk.Label(frameScan,text=labelsScan[i],background=bgColor,foreground=cColor)
        label.grid(row=[i],column=0)
        entriesScan=np.append(entriesScan,tk.Entry(frameScan,width=10))
        entriesScan[i].grid(row=[i],column=1,sticky=tk.EW)
        entriesScan[i].delete(0,tk.END)
        entriesScan[i].insert(tk.END,initialsScan[i])
        label = tk.Label(frameScan,text=unitsScan[i],background=bgColor,foreground=cColor)
        label.grid(row=[i],column=2)
    for i in np.arange(np.size(labelsHV)):
        label = tk.Label(frameHV,text=labelsHV[i],background=bgColor,foreground=cColor)
        label.grid(row=[i],column=0)
        entriesHV=np.append(entriesHV,tk.Entry(frameHV,width=10))
        entriesHV[i].grid(row=[i],column=1,sticky=tk.EW)
        entriesHV[i].delete(0,tk.END)
        entriesHV[i].insert(tk.END,initialsHV[i])
        label = tk.Label(frameHV,text=unitsHV[i],background=bgColor,foreground=cColor)
        label.grid(row=[i],column=2)
    for i in np.arange(np.size(labelsFix)):
        label = tk.Label(frameFix,text=labelsFix[i],background=bgColor,foreground=cColor)
        label.grid(row=[i],column=0)
        entriesFix=np.append(entriesFix,tk.Entry(frameFix,width=10))
        entriesFix[i].grid(row=[i],column=1,sticky=tk.EW)
        entriesFix[i].delete(0,tk.END)
        entriesFix[i].insert(tk.END,initialsFix[i])
        label = tk.Label(frameFix,text=unitsFix[i],background=bgColor,foreground=cColor)
        label.grid(row=[i],column=2)
    for i in np.arange(np.size(labelsDMA)):
        label = tk.Label(frameDMA,text=labelsDMA[i],background=bgColor,foreground=cColor)
        label.grid(row=[i],column=0)
        entriesDMA=np.append(entriesDMA,tk.Entry(frameDMA,width=10))
        entriesDMA[i].grid(row=[i],column=1,sticky=tk.EW)
        entriesDMA[i].delete(0,tk.END)
        entriesDMA[i].insert(tk.END,initialsDMA[i])
        label = tk.Label(frameDMA,text=unitsDMA[i],background=bgColor,foreground=cColor)
        label.grid(row=[i],column=2)

    # File control
    entriesFileName=tk.Entry(frameFile,width=50)
    entriesFileName.grid(row=0,column=1,sticky=tk.EW)
    for i in [0,2,4]:
        tk.Label(frameFile,text=" ",background=bgColor).grid(row=0,column=i)
    def select_file():
        filename = fd.askopenfilename(title='Open a file',initialdir='/Users/tamat/HV/DMAscan/')
        showinfo(title='Selected File',message=filename)
        entriesFileName.delete(0,tk.END)
        entriesFileName.insert(tk.END,filename)

    open_button = tk.Button(frameFile,text='Select a File',command=select_file)
    open_button.grid(row=0,column=3,sticky=tk.EW)


    # Generate DMA class
    dma=DMA.DMAscan(entriesDAQ,entriesScan,entriesHV,entriesFileName)

    # function to stop/start scan
    def stopScan():
        dma.stop=1
    def startScan():
        dma.setVal(entriesDAQ,entriesScan,entriesHV,entriesFileName)
        thread = threading.Thread(target=dma.scan)
        thread.start()
    def startFixV():
        dma.setVal(entriesDAQ,entriesScan,entriesHV,entriesFileName)
        dma.cpc.mode=int(entriesFix[1].get())
        thread = threading.Thread(target=dma.hv.HVout(float(entriesFix[0].get())))
        thread.start()

    # generate stop/start buttons
    stop=tk.Button(frameScan,text="Stop",background="blue4",foreground=cColor,width=20,height=2,command=lambda:stopScan())
    stop.grid(row=np.size(labelsScan)+1,column=0,columnspan=3)
    start=tk.Button(frameScan,text="Start DMA scan",background="blue4",foreground=cColor,width=20,height=2,command=lambda:startScan())
    start.grid(row=np.size(labelsScan),column=0,columnspan=3)
    stopFix=tk.Button(frameFix,text="Stop",background="blue4",foreground=cColor,width=20,height=2,command=lambda:stopScan())
    stopFix.grid(row=np.size(labelsFix)+1,column=0,columnspan=3)
    startFix=tk.Button(frameFix,text="Start",background="blue4",foreground=cColor,width=20,height=2,command=lambda:startFixV())
    startFix.grid(row=np.size(labelsFix),column=0,columnspan=3)


    frameDAQ.grid_columnconfigure(1, weight=1)
    frameDAQ.grid_rowconfigure(list(range(np.size(labelsDAQ))), weight=1)
    frameScan.grid_columnconfigure(1, weight=1)
    frameScan.grid_rowconfigure(list(range(np.size(labelsScan)+2)), weight=1)
    frameHV.grid_columnconfigure(1, weight=1)
    frameHV.grid_rowconfigure(list(range(np.size(labelsHV))), weight=1)
    frameFile.grid_columnconfigure(1, weight=1)
    frameFile.grid_rowconfigure(list(range(1)), weight=1)
    frameFix.grid_columnconfigure(1, weight=1)
    frameFix.grid_rowconfigure(list(range(np.size(labelsFix)+2)), weight=1)
    frameDMA.grid_columnconfigure(1, weight=1)
    frameDMA.grid_rowconfigure(list(range(np.size(labelsDMA))), weight=1)

    def update():
        if(dma.updateFlag):
            dma.figUpdate(window)
            dma.updateFlag=0
        window.after(1000, update)
    update()

    window.mainloop()

if __name__ == "__main__":
    main()

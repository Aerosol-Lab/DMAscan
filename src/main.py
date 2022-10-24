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
    window.geometry("1000x600")
    window.configure(bg=bgColor)

    frameDAQ=tk.LabelFrame(window,text="DAQ settings",font=("",15),background=bgColor,foreground="white")
    frameDAQ.place(x=10,y=10,width=195,height=200)
    frameScan=tk.LabelFrame(window,text="Scan mode",font=("",15),background=bgColor,foreground="white")
    frameScan.place(x=220,y=10,width=195,height=305)
    frameHV=tk.LabelFrame(window,text="HV parameters",font=("",15),background=bgColor,foreground="white")
    frameHV.place(x=10,y=220,width=195,height=100)
    frameFile=tk.LabelFrame(window,text="File setting",font=("",15),background=bgColor,foreground="white")
    frameFile.place(x=10,y=520,width=300,height=70)

    labelsDAQ=np.array(["CPC connection","V_CPC min","V_CPC max","HV connection","V_HV min","V_HV max"])
    labelsScan=np.array(["Min voltage","Max voltage","Time per a bin","Number of bins","Delay time","HV mode","CPC mode"])
    labelsHV=np.array(["Slope","Bias"])
    unitsDAQ=np.array([" ","V","V"," ","V","V"])
    unitsScan=np.array(["V","V","s"," ","s"," "," "])
    unitsHV=np.array([" ","V"])
    initialsDAQ=np.array(["Dev1/ai0",0,10,"Dev1/ao1",0,5])
    initialsScan=np.array([10,1000,5,10,2,0,-1])
    initialsHV=np.array([2000,0])

    entriesDAQ=[]
    entriesScan=[]
    entriesHV=[]
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

    dma=DMA.DMAscan(entriesDAQ,entriesScan,entriesHV)

    def stopScan():
        dma.stop=1

    def startScan():
        dma.setVal(entriesDAQ,entriesScan,entriesHV)
        thread = threading.Thread(target=dma.scan)
        thread.start()

    stop=tk.Button(frameScan,text="Stop",background="blue4",foreground=cColor,width=20,height=2,command=lambda:stopScan())
    stop.grid(row=np.size(labelsScan)+1,column=0,columnspan=3)

    start=tk.Button(frameScan,text="Start DMA scan",background="blue4",foreground=cColor,width=20,height=2,command=lambda:startScan())
    start.grid(row=np.size(labelsScan),column=0,columnspan=3)

    frameDAQ.grid_columnconfigure(1, weight=1)
    frameDAQ.grid_rowconfigure(list(range(np.size(labelsDAQ))), weight=1)
    frameScan.grid_columnconfigure(1, weight=1)
    frameScan.grid_rowconfigure(list(range(np.size(labelsScan)+2)), weight=1)
    frameHV.grid_columnconfigure(1, weight=1)
    frameHV.grid_rowconfigure(list(range(np.size(labelsHV))), weight=1)

    def update():
        if(dma.updateFlag):
            dma.figUpdate(window)
            dma.updateFlag=0
        window.after(1000, update)

    update()

    entriesFileName=tk.Entry(frameFile,width=10)
    entriesFileName.grid(row=0,column=0,sticky=tk.EW)

    def select_file():
        filename = fd.askopenfilename(title='Open a file',initialdir='/Users/tamat/HV/DMAscan/')
        showinfo(title='Selected File',message=filename)
        entriesFileName.delete(0,tk.END)
        entriesFileName.insert(tk.END,filename)

    open_button = tk.Button(frameFile,text='Select a File',command=select_file)
    open_button.grid(row=0,column=1,sticky=tk.EW)

    window.mainloop()

if __name__ == "__main__":
    main()

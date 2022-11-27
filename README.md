# DMA-CPC control with DAQ (NI)
## 1. Overview
This code is able to be utilized for controling differential mobility analyzer (DMA) and condensation particle conuter (CPC) which is known as scaning mobility particle sizer (SMPS, a particle size distribution measurements in gas).  This code works with GUI as desplayed in this figure.

## 2. Usage
### 2.1. Executable version
#### Preparation  
1. Download binary file `DMACPC.exe` from [here](https://drive.google.com/drive/u/1/folders/1Ji9DRLZVkaaNpGYrlUw99TsapHkMQL9J) or email to us (the address is at the bottom of this page) if you don't have an access.
2. Download NI-DAQ driver from [here](https://www.ni.com/en-us/support/downloads/drivers/download.ni-daqmx.html#460239) and install it (it just follow their instruction).  
#### Usage
1. Double click `DMACPC.exe` file
2. Set the device name and port to use.  Default value is Dev1/ai0 for the reading from CPC and Dev1/ao1 for sending control signal to high voltage source.  Device name is obtained from "NI Device Monitor" when the device is connected with your PC via usb cable.  
...

### 2.2. Run from source code
* For Anaconda user (you can get Anaconda from [here](https://www.anaconda.com/))
Most of labraries are installed for Anaconda user case but you only need to download NI-DAQ driver from this [link](https://www.ni.com/en-us/support/downloads/drivers/download.ni-daqmx.html#460239).  After the installation, you can run `HV.py` from any console like Powershell Prompt or JupyterLab.
* For not Anaconda user
You need to install the modules if it isn't: Numpy, Tkinter, Matplotlib, and [NI-DAQ driver](https://www.ni.com/en-us/support/downloads/drivers/download.ni-daqmx.html#460239), then you can run `HV.py`.  Here, the explanation is brielf since "not Anaconda" user may know a lot how to install and use it.

# Author
* Dr. Tomoya Tamadate
* Hogan Lab.
* [Home page](https://hoganlab.umn.edu/)/[LinkedIn](https://www.linkedin.com/in/hogan-lab-994a3a246/)
* University of Minnesota
* HoganLaboratory[at]umn.edu

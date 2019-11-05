# -*- coding: utf-8 -*-
import numpy as np #usado para gerar um array com os valores medidos
import pandas as pd #usado para guardar os valores medidos
import time #adicionar dalys
import matplotlib.pyplot as plt #plotar gráficos
from scipy.stats import linregress
import spidev #comunicação spi

#início da comunicação SPI
spi0 = spidev.SpiDev() #cria um objeto
spi0.open(0,0)

spi1 = spidev.SpiDev()
spi1.open(0,1)#open spi1 on bus 0 cs 1

results0 = pd.DataFrame()
results1 = pd.DataFrame()
loads = np.arange(0,20+2,2)


for load in loads:

    #leitura dos dados do MCP3008
    def analogInput0(channel):
      spi0.max_speed_hz = 1350000
      adc = spi0.xfer2([1,(8+channel)<<4,0])
      data = ((adc[1]&3) << 8) + adc[2]
      return data
    data0 = analogInput0(0)
    
    def analogInput1(channel):
      spi1.max_speed_hz = 1350000
      adc = spi1.xfer2([2,(8+channel)<<2,0])
      data = ((adc[2]&3) << 8) + adc[2]
      return data
    data1 = analogInput1(1)

    #conversão dos dados em tensão 3.3V
    def Volts3(data0):
      volts0 = (data0 * 3.3) / float(1023)
      volts0 = round(volts0, 2) # Round off to 2 decimal places
      return volts0
    volt0 = Volts3(data0)
    
    def Volts5(data1):
        volts1 = (data1 * 5) / float(1023)
        volts1 = round(volts1, 2) # Round off to 2 decimal places
        return volts1
    volt1 = Volts5(data1)

    time.sleep(2)

    temp0= {}
    temp1={}
    temp0['Vout'] = float(volt0)
    temp1['Vusb'] = float(volt1)
    temp0['Iout'] = float(volt0)/100

    temp0['Vout_id'] = 3.3
    temp1['Vusb_id'] = 5
    temp0['Vout_err'] = temp0['Vout_id'] - temp0['Vout']
    temp1['Vusb_err'] = temp1['Vusb_id'] - temp1['Vusb']
    temp0['Pass'] = 'Yes'
    if (abs(temp0['Vout_err'])> temp0['Vout_id']*0.001): #1% de tolerância
        temp0['Pass'] = 'No'
    if (abs(temp1['Vusb_err'])> temp1['Vusb_id']*0.001): #1% de tolerância
        temp1['Pass'] = 'No'

    results0 = results0.append(temp0, ignore_index=True)
    results1 = results1.append(temp1, ignore_index=True)
    

results0.to_csv('Results0.csv')
results1.to_csv('Results1.csv')

loadline0 = linregress(results0['Iout'], results0['Vout'])


plt.plot(results0['Iout'], results0['Vout'], 'ro')
plt.show()

    


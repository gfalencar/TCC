# -*- coding: utf-8 -*-
import numpy as np #usado para gerar um array com os valores medidos
import pandas as pd #usado para guardar os valores medidos
import time #adicionar dalys
import matplotlib.pyplot as plt #plotar gráficos
from scipy.stats import linregress
import spidev #comunicação spi

#início da comunicação SPI
spi = spidev.SpiDev() #cria um objeto
spi.open(0,0)

results = pd.DataFrame()
loads = np.arange(0,20+2,2)


for load in loads:

    #leitura dos dados do MCP3008
    def analogInput(channel):
      spi.max_speed_hz = 1350000
      adc = spi.xfer2([1,(8+channel)<<4,0])
      data = ((adc[1]&3) << 8) + adc[2]
      return data
    data = analogInput(1)

    #conversão dos dados em tensão
    def Volts(data):
      volts = (data * 3.3) / float(1023)
      volts = round(volts, 2) # Round off to 2 decimal places
      return volts
    volt = Volts(data)

    time.sleep(2)

    temp= {}
    temp['Vout'] = float(volt)
    temp['Iout'] = float(volt)/100

    temp['Vout_id'] = 3.3
    temp['Vout_err'] = temp['Vout_id'] - temp['Vout']
    temp['Pass'] = 'Yes'
    if (abs(temp['Vout_err'])> temp['Vout_id']*0.001): #1% de tolerância
        temp['Pass'] = 'No'

    results = results.append(temp, ignore_index=True)
    #print "%.2fA\t%.3fV" % (temp['Iout'], temp['Vout'])

results.to_csv('Results.csv')

loadline = linregress(results['Iout'], results['Vout'])
#print "The loadline is %.2f mohm" % (loadline[0]*1000)
#print "The intercept point is %.3V" % loadline[1]

plt.plot(results['Iout'], results['Vout'], 'ro')
plt.show()

    


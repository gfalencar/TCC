# -*- coding: utf-8 -*-
import numpy as np #usado para gerar um array com os valores medidos
import pandas as pd #usado para guardar os valores medidos
import time #adicionar dalys
import matplotlib.pyplot as plt #plotar gráficos
from scipy.stats import linregress
import spidev #comunicação spi
import RPi.GPIO as GPIO

#início da comunicação SPI
spi = spidev.SpiDev() #cria um objeto
spi.open(0,0)
speed = 200000
#1000000
spi.max_speed_hz=speed

results0 = pd.DataFrame()
results1 = pd.DataFrame()
loads = np.arange(0,20+2,2)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)


for load in loads:
    
    # Função para leitura dos dados SPI do MCP3208
    # Channel é um numero inteiro de 0 a 7
    def ReadChannel(channel):
      adc = spi.xfer2([1,(8+channel)<<4,0])
      data = ((adc[1]&3) << 8) + adc[2]
      return data
    
    # Função para converter os dados em tensão
    # deci especifica o numero de casas decimais para arredondar.
    def ConvertVolts3(data,deci):
      volts = (data * 3.3) / float(1023)
      volts = round(volts,deci)
      return volts
    
    def ConvertVolts5(data,deci):
      volts = (data * 5) / float(1023)
      volts = round(volts,deci)
      return volts
    
    #Definição de qual canal de leitura do MCP3208
    volt3_channel = 0
    volt5_channel  = 1
    volt3carga_channel = 2
    
    # Leitura da saída 3.3V do Regulador
    volt3_data = ReadChannel(volt3_channel)
    vout = ConvertVolts3(volt3_data,3)
    vload_data = ReadChannel(volt3carga_channel)
    vload = ConvertVolts3(vload_data,3)
 
    # Leitura da entrada 5V do Regulador
    volt5_data = ReadChannel(volt5_channel)
    vin = ConvertVolts5(volt5_data,3)
 
    #print("--------------------------------------------")
    print("Vout: {} ({}V)".format(volt3_data,vout))
    print("Vin : {} ({}V)".format(volt5_data,vin))

    time.sleep(5)
    
    #Preenchimento dos dados na tabela
    temp0= {}
    temp0['Vout'] = float(vout)
    temp0['Vusb'] = float(vin)
    temp0['Vload'] = float(vload)
    temp0['Iout'] = float(vload)/330
    temp0['Vout_id'] = 3.3 #Vout ideal
    temp0['Vusb_id'] = 5 #Vin ideal
    temp0['Vout_err'] = temp0['Vout_id'] - temp0['Vout']
    temp0['Vusb_err'] = temp0['Vusb_id'] - temp0['Vusb']
    
    temp0['Pass'] = 'Yes'
    if (abs(temp0['Vout_err'])> temp0['Vout_id']*0.001 and abs(temp0['Vusb_err'])> temp0['Vusb_id']*0.001): #1% de tolerância
        temp0['Pass'] = 'No'
    #if (abs(temp0['Vusb_err'])> temp0['Vusb_id']*0.001): #1% de tolerância
        #temp0['Pass'] = 'No'

    results0 = results0.append(temp0, ignore_index=True)
    
    #Chaveamento para mudançade carga na saída 3.3V
    GPIO.output(5, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(5, GPIO.LOW)
    
    #GPIO.output(6, GPIO.HIGH)
    #time.sleep(1)
    #GPIO.output(6, GPIO.LOW)
    
    #GPIO.output(13, GPIO.HIGH)
    #time.sleep(1)
    #GPIO.output(13, GPIO.LOW)
    
    

results0.to_csv('Results0.csv')
#results1.to_csv('Results1.csv')

loadline0 = linregress(results0['Iout'], results0['Vout'])


plt.plot(results0['Iout'], results0['Vout'], 'ro')
plt.show()

    


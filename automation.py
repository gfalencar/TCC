# -*- coding: utf-8 -*-
import numpy as np #usado para gerar um array com os valores medidos
import pandas as pd #usado para guardar os valores medidos
import time #adicionar dalys
import matplotlib.pyplot as plt #plotar gráficos
from scipy.stats import linregress
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 # Import the ADS1x15 module.


results0 = pd.DataFrame()
results1 = pd.DataFrame()
loads = np.arange(0,20+2,2)
t = np.arange(0.0, 11.0, 1)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

adc = Adafruit_ADS1x15.ADS1115()

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 2/3


for load in loads:
    
    print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
    print('-' * 37)
    # Read all the ADC channel values in a list.
    values = [0]*4
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values[i] = adc.read_adc(i, gain=GAIN)
        # Note you can also pass in an optional data_rate parameter that controls
        # the ADC conversion time (in samples/second). Each chip has a different
        # set of allowed data rate values, see datasheet Table 9 config register
        # DR bit values.
        #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        # Each value will be a 12 or 16 bit signed integer value depending on the
        # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
    # Print the ADC values.
    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    # Pause for half a second.
    
    def ConvertVolts3(values,deci):
      volts = (values * 3.3) / float(17551)
      volts = round(volts,deci)
      return volts
    
    vout = ConvertVolts3(values[0],4)
    print(vout)
    

    
    # Função para converter os dados em tensão
    # deci especifica o numero de casas decimais para arredondar.
    #def ConvertVolts3(data,deci):
      #volts = (data * 3.3) / float(1023)
      #volts = round(volts,deci)
      #return volts
    
    def ConvertVolts5(values,deci):
      volts = (values * 5) / float(20486)
      volts = round(volts,deci)
      return volts
    
    vin = ConvertVolts5(values[1],4)
    print(vin)
    

    time.sleep(0.1)
    
    #Preenchimento dos dados na tabela
    temp0= {}
    temp0['Vout'] = float(vout)
    temp0['Vusb'] = float(vin)
    #temp0['Vload'] = float(vload)
    #temp0['Iout'] = float(vload)/330
    temp0['Vout_id'] = 3.3000 #Vout ideal
    temp0['Vusb_id'] = 5.0000 #Vin ideal
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

#loadline0 = linregress(results0['Iout'], results0['Vout'])


plt.figure()
plt.subplot(211)
plt.xlabel('Tempo(s)')
plt.ylabel('Tensão(V)')
plt.plot(t, results0['Vout'])
plt.title('Tensão de saída 3.3V')

plt.subplot(212)
plt.xlabel('Tempo(s)')
plt.ylabel('Tensão(V)')
plt.plot(t, results0['Vusb'])
plt.title('Tensão de entrada 5V')


#plt.subplot(213)
#plt.plot(t, results0['Vload'], 'ro')
#plt.title('Tensão de saída 3.3V com carga')
plt.show()

    


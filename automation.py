# -*- coding: utf-8 -*-
import numpy as np #USADO PARA GERAÇÃO DE ARRAYS COM OS VALORES MEDIDOS
import pandas as pd #USADO PARA ANALISE/AMARZENAMETO DOS DADOS EM TABELAS
import time #ADCIONAR DELAYS
import matplotlib.pyplot as plt #PLOTAR GRÁFICOS
from scipy.stats import linregress
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 #BIBLIOTECA PARA O ADC ADS115

#TABELA PARA ARMAZNAR VALORE MEDIDOS
temp0= {}
results0 = pd.DataFrame(temp0, columns=['Vin Ideal','Vin Medido', 'Erro Vin','Vout Ideal','Vout Medido', 'Erro Vout', 'Vload','Resultado Teste'])
loads = np.arange(0,100+1,1)
t = np.arange(0.0, 101, 1)


#CONFIRGURAÇÃO DOS GPIOS
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(5, GPIO.OUT) #GPIO PARA A CARGA NA SAIDA 3.3V

#PINOS PARA TESTE DOS GPIOS MONTAGEM PROTOBOARD
#OUTPUT_PIN_D5 = 4           
#INPUT_PIN_D6 = 17
#INPUT_PIN_D9 = 18
#INPUT_PIN_D10 = 22
#INPUT_PIN_D11 = 23
#INPUT_PIN_D12 = 24
#INPUT_PIN_D13 = 25
#GPIO.setup(OUTPUT_PIN_D5, GPIO.OUT) 
#GPIO.setup(INPUT_PIN_D6, GPIO.IN)
#GPIO.setup(INPUT_PIN_D9, GPIO.IN)
#GPIO.setup(INPUT_PIN_D10, GPIO.IN)
#GPIO.setup(INPUT_PIN_D11, GPIO.IN)
#GPIO.setup(INPUT_PIN_D12, GPIO.IN)
#GPIO.setup(INPUT_PIN_D13, GPIO.IN)

#PINOS PARA TESTE DOS GPIOS MONTAGEM PCB

OUTPUT_PIN_D5 = 19           
INPUT_PIN_D6 = 13
INPUT_PIN_D9 = 6
INPUT_PIN_D10 = 7
INPUT_PIN_D11 = 11
INPUT_PIN_D12 = 9
INPUT_PIN_D13 = 24
GPIO.setup(OUTPUT_PIN_D5, GPIO.OUT) 
GPIO.setup(INPUT_PIN_D6, GPIO.IN)
GPIO.setup(INPUT_PIN_D9, GPIO.IN)
GPIO.setup(INPUT_PIN_D10, GPIO.IN)
GPIO.setup(INPUT_PIN_D11, GPIO.IN)
GPIO.setup(INPUT_PIN_D12, GPIO.IN)
GPIO.setup(INPUT_PIN_D13, GPIO.IN)



#GANHO DO ADC: DE ACORDO COM O DATASHEET PARA MUDAR O RANGE DAS TENSÕES LIDAS - GAIN=2/3 -> +/-6.144V
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 2/3

#CHAVEAMENTO PARA MUDANÇA DE CARGA NA SAIDA 3.3V COM UM TBJ
GPIO.output(5, GPIO.HIGH)

# FUNÇÃO PARA CONVERTER OS DADOS DA LEITURA DO ADC EM TENSÃO

def ConvertVolts3(values,deci):
    volts = (values * 3.3) / float(17551)
    volts = round(volts,deci)
    return volts
    
def ConvertVolts5(values,deci):
    volts = (values * 5) / float(20486)
    volts = round(volts,deci)
    return volts


for load in loads:
    
    #LEITURA DOS CANAIS DO ADC EM UMA LISTA
    values = [0]*4
    for i in range(4):
        values[i] = adc.read_adc(i, gain=GAIN)
    
    #CANAL 0 = 3.3V (VOUT)
    #CANAL 1 = 5V (VIN)
    #CANAL 2 = 3.3V (VLOAD)
    vout = ConvertVolts3(values[0],4)
    vin = ConvertVolts5(values[1],4)
    vload = ConvertVolts3(values[2],4)

    
    #PREENCHIMENTO DAS MEDIÇÕES NA TABELA
    
    temp0['Vout Medido'] = float(vout)
    temp0['Vin Medido'] = float(vin)
    temp0['Vload'] = float(vload)
    temp0['Vout Ideal'] = 3.300 #VOUT IDEAL
    temp0['Vin Ideal'] = 5.000 #VIN IDEAL
    temp0['Erro Vout'] = temp0['Vout Ideal'] - temp0['Vout Medido']
    temp0['Erro Vin'] = temp0['Vin Ideal'] - temp0['Vin Medido']
    
    temp0['Resultado Teste'] = 'PASS'
    if (abs(temp0['Erro Vout'])> 0.097515):
        #+1.5% ACURÁCIA DATASHEET Verr = 0.0495
        #+2.955% ACURÁCIA CALCULADA Verr = 0.097515
        temp0['Resultado Teste'] = 'FAIL'

    results0 = results0.append(temp0, ignore_index=True)

results0.to_csv('Results0.csv')

#TABELAS COM VALORES MÉDIOS, MINIMOS E MÁXIMOS.

temp1={}
resultsvin = pd.DataFrame(temp1, columns=['Média Vin', 'Maximo Vin', 'Minimo Vin'])
temp1['Média Vin'] = results0['Vin Medido'].mean()
temp1['Minimo Vin'] = results0['Vin Medido'].min()
temp1['Maximo Vin'] = results0['Vin Medido'].max()
resultsvin = resultsvin.append(temp1, ignore_index=True)
resultsvin.to_csv('Resultsvin.csv')

temp2={}
resultsvout = pd.DataFrame(temp2, columns=['Média Vout', 'Maximo Vout', 'Minimo Vout'])
temp2['Média Vout'] = results0['Vout Medido'].mean()
temp2['Minimo Vout'] = results0['Vout Medido'].min()
temp2['Maximo Vout'] = results0['Vout Medido'].max()
resultsvout = resultsvout.append(temp2, ignore_index=True)
resultsvout.to_csv('Resultsvout.csv')

temp3={}
resultsvload = pd.DataFrame(temp3, columns=['Média Vload', 'Maximo Vload', 'Minimo Vload'])
temp3['Média Vload'] = results0['Vload'].mean()
temp3['Minimo Vload'] = results0['Vload'].min()
temp3['Maximo Vload'] = results0['Vload'].max()
resultsvload = resultsvload.append(temp3, ignore_index=True)
resultsvload.to_csv('Resultsvload.csv')

#loadline0 = linregress(results0['Iout'], results0['Vout'])

GPIO.output(5, GPIO.LOW)

#TABELA PARA ANALISE DOS GPIOS
pins = [INPUT_PIN_D6, INPUT_PIN_D9, INPUT_PIN_D10, INPUT_PIN_D11, INPUT_PIN_D12, INPUT_PIN_D13];
temp4={}
resultsgpio = pd.DataFrame(temp4, columns=['D6','D9', 'D10','D11','D12', 'D13'])
status = np.arange(0,5+1,1)


for pin in status:
        
    GPIO.output(OUTPUT_PIN_D5, 1)
    time.sleep(0.5);
               
    if (GPIO.input(INPUT_PIN_D6) == True):
        temp4['GPIO D6'] = 'D6 ON'
        print('D6 ON')
        
    else:
        temp4['GPIO D6'] = 'D6 OFF'
        print('D6 OFF')
              
        
    if (GPIO.input(INPUT_PIN_D9) == True):
        temp4['GPIO D9'] = 'D9 ON'
        print('D9 ON')
    else:
        temp4['GPIO D9'] = 'D9 OFF'
        print('D9 OFF')
        
            
    if (GPIO.input(INPUT_PIN_D10) == True):
        temp4['GPIO D10'] = 'D10 ON'
        print('D10 ON')
            
    else:
        temp4['GPIO D10'] = 'D10 OFF'
        print('D10 OFF')
        
        
    if (GPIO.input(INPUT_PIN_D11) == True):
        temp4['GPIO D11'] = 'D11 ON'
        print('D11 ON')
    else:
        temp4['GPIO D11'] = 'D11 OFF'
        print('D11 OFF')
        
                       
    if (GPIO.input(INPUT_PIN_D12) == True):
        temp4['GPIO D12'] = 'D12 ON'
        print('D12 ON')
    else:
        temp4['GPIO D12'] = 'D12 OFF'
        print('D12 OFF')
        
                            
    if (GPIO.input(INPUT_PIN_D13) == True):
        temp4['GPIO D13'] = 'D13 ON'
        print('D13 ON')
    else:
        temp4['GPIO D13'] = 'D13 OFF'
        print('D13 OFF')
    print('----------------------------------')
    time.sleep(1.7);
    
    GPIO.output(OUTPUT_PIN_D5, 0)
    
    resultsgpio = resultsgpio.append(temp4, ignore_index=True)
    

resultsgpio.to_csv('ResultsGPIO1.csv')

#GRÁFICOS DE VIN E VOUT

plt.figure()
plt.subplot(211)
plt.xlabel('Tempo(s)')
plt.ylabel('Tensão(V)')
plt.ylim((3.2899,3.5999))
plt.plot(t, results0['Vout Medido'])
plt.title('Tensão de saída 3.3V')

plt.subplot(212)
plt.xlabel('Tempo(s)')
plt.ylabel('Tensão(V)')
plt.ylim((4.100,5.199))
plt.plot(t, results0['Vin Medido'])
plt.title('Tensão de entrada 5V')

plt.show()
    


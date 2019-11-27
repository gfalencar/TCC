from time import sleep           # Allows us to call the sleep function to slow down our loop
import RPi.GPIO as GPIO           # Allows us to call our GPIO pins and names it just GPIO
import numpy as np #usado para gerar um array com os valores medidos
import pandas as pd #usado para guardar os valores medidos
 

GPIO.setmode(GPIO.BCM)           # Set's GPIO pins to BCM GPIO numbering
OUTPUT_PIN_D5 = 4           
INPUT_PIN_D6 = 17
INPUT_PIN_D9 = 18
INPUT_PIN_D10 = 22
INPUT_PIN_D11 = 23
INPUT_PIN_D12 = 24
INPUT_PIN_D13 = 25
GPIO.setup(OUTPUT_PIN_D5, GPIO.OUT) # Set our input pin to be an input
GPIO.setup(INPUT_PIN_D6, GPIO.IN)
GPIO.setup(INPUT_PIN_D9, GPIO.IN)
GPIO.setup(INPUT_PIN_D10, GPIO.IN)
GPIO.setup(INPUT_PIN_D11, GPIO.IN)
GPIO.setup(INPUT_PIN_D12, GPIO.IN)
GPIO.setup(INPUT_PIN_D13, GPIO.IN)

pins = [INPUT_PIN_D6, INPUT_PIN_D9, INPUT_PIN_D10, INPUT_PIN_D11, INPUT_PIN_D12, INPUT_PIN_D13];
results1 = pd.DataFrame()
status = np.arange(0,5+1,1)


for pin in status:
    temp1={}
        
    GPIO.output(OUTPUT_PIN_D5, 1)
    sleep(0.5);
               
    if (GPIO.input(INPUT_PIN_D6) == True):
        temp1['GPIO D6'] = 'D6 ON'
        print('D6 ON')
        
    else:
        temp1['GPIO D6'] = 'D6 OFF'
        print('D6 OFF')
              
        
    if (GPIO.input(INPUT_PIN_D9) == True):
        temp1['GPIO D9'] = 'D9 ON'
        print('D9 ON')
    else:
        temp1['GPIO D9'] = 'D9 OFF'
        print('D9 OFF')
        
            
    if (GPIO.input(INPUT_PIN_D10) == True):
        temp1['GPIO D10'] = 'D10 ON'
        print('D10 ON')
            
    else:
        temp1['GPIO D10'] = 'D10 OFF'
        print('D10 OFF')
        
        
    if (GPIO.input(INPUT_PIN_D11) == True):
        temp1['GPIO D11'] = 'D11 ON'
        print('D11 ON')
    else:
        temp1['GPIO D11'] = 'D11 OFF'
        print('D11 OFF')
        
                       
    if (GPIO.input(INPUT_PIN_D12) == True):
        temp1['GPIO D12'] = 'D12 ON'
        print('D12 ON')
    else:
        temp1['GPIO D12'] = 'D12 OFF'
        print('D12 OFF')
        
                            
    if (GPIO.input(INPUT_PIN_D13) == True):
        temp1['GPIO D13'] = 'D13 ON'
        print('D13 ON')
    else:
        temp1['GPIO D13'] = 'D13 OFF'
        print('D13 OFF')
    print('----------------------------------')
    sleep(1.7);
    
    GPIO.output(OUTPUT_PIN_D5, 0)
    
    results1 = results1.append(temp1, ignore_index=True)
    

results1.to_csv('ResultsGPIO.csv')


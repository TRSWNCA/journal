# Journal

## 2021

### 5.23

**pandas plot**

Use pandas to draw picture

```python
#/usr/bin/python

import pandas as pd
import matplotlib.pyplot as plt

file = open('result.txt', 'r')

lines = file.readlines()

train_data = []
test_data = []

for line in lines:
    if line[1] == 'r': # train
        train_data.append(float(line.split()[-1]))
    else: # test
        test_data.append(float(line.split()[-1]))

train_set = pd.Series(train_data)
test_set = pd.Series(test_data)

train_set.plot(title = 'IWAU-Net diceloss', legend = True, label = 'train diceloss')
test_set.plot(legend = True, label = 'test diceloss')

plt.savefig('result.png')
```

**count down helper**

In order to train my coding speed, write a count down helper.

Think twice code once.

```python
#!/usr/bin/python3                                                                                                      
# -*- coding: UTF-8 -*-                                                                                         
import time  
import shutil                                                                                                           
                                                                                                                       
def countdown(m):
    colums = shutil.get_terminal_size().columns                                                                         
    m = int(m)                                                                                                          
    for minute in range(m, -1, -1):                                                                                     
        if minute == 0:                                                                      
            break                                                        
        for second in range(59, -1, -1):                                                                               
            time.sleep(1)  
            sys.stdout.write("\r")                       
            sys.stdout.write(('{}:{}'.format(minute-1, second)).center(colums))                                         
            sys.stdout.flush()                                                                                         
                                                                                                                        
    sys.stdout.write(('END')).center(colums))                                                                           
                                                                                                                        
if __name__ == '__main__':                                                                                              
    countdown(sys.argv[1])
```

### 5.24

Install Latex on Ubuntu 18.04:

```bash
sudo apt-get install texlive-full
```

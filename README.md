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
                                                                                                                        
    sys.stdout.write(('END').center(colums))                                                                           
                                                                                                                        
if __name__ == '__main__':                                                                                              
    countdown(sys.argv[1])
```

### 5.24

Install Latex on Ubuntu 18.04:

```bash
sudo apt-get install texlive-full
```

### 5.26

Program to help merge excel forms.

Use `pandas` and its data frame to work.

To read .xlsx need to use xrld <= 1.2.0

```bash
pip uninstall xlrd
pip install xlrd==1.2.0
```

```python
import pandas as pd
import os
pathDir = os.listdir('data')

def solve(filename):
    global al
    print("On: ", filename)
    fi = pd.read_excel('data/' + filename, index_col = 1) #, converters = {'学号' : str})
    stu = fi.index
    teacher = filename.split('.')[0]
    for person in stu:
        print(person)
        al.loc[person, '最终成绩'] = fi.loc[person, '最终成绩'] #fi.loc[person, '最终成绩']
        al.loc[person, '批卷人'] = teacher

    print("Read: ", fi.shape)


if __name__ == '__main__':
    global al
    al = pd.read_excel('2021毕业学生名单.xls', index_col = 0) #, converters = {'学号' : str})
    al['批卷人'] = 'unkown'
    for x in pathDir:
        solve(x)
    writer = pd.ExcelWriter('result.xls')
    al.to_excel(writer)
    writer.save()

```

However its converters dont work, use dtype to replace it.

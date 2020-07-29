import os
import time 
import datetime 
  


fname = 'datasets_8388_11883_IBM_2006-01-01_to_2018-01-01.csv'
with open(fname, 'a+') as f:  
    first_line = f.readline()
    off = -250
    f.seek(0, os.SEEK_END)
    f.seek(f.tell()+off, os.SEEK_SET) 
    last_line = f.readlines()[-1].split(',')
    lasttime = datetime.datetime.strptime(last_line[0],"%Y-%m-%d") 
    modified_date = lasttime + datetime.timedelta(days=1);
    last_line[0]=modified_date.strftime("%Y-%m-%d")

    f.seek(0, os.SEEK_END)
    f.write(last_line[0])

    for i in range(1,len(last_line)):
        f.write(','+last_line[i])
    print(last_line)
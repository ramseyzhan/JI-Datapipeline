import datetime
from datetime import datetime

# data[i][0] time     '2006-12-20 04:00:00'    最好可以直接是时间戳 1166605200
# data[i][1] actual val
# data[i][2] predic val

def read():
	data=[]
	count=-1;
	with open("first-200.txt") as f:
		for line in f.readlines():
			count= (count+1) %4;

			if(count==0):
				cur = [datetime.strptime(line, '%Y-%m-%d %H:%M:%S\n').replace().timestamp()*1000]
			elif(count==1):
				cur.append(float(line.split('[')[1].split()[0]))
			elif(count==3):
				cur.append(float(line))
				data.append(cur)
	print(data);

def gen(data,std,threshold):
	pass


read();
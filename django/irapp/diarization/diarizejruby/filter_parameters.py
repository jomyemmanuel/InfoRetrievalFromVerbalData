
def filterout(path):
	f=open(path,'r')
	d={}
	l=[lines for lines in f.readlines()]
	length=len(l)
	for pos in xrange(0,length/3):
		speaker =l[pos]
		duration=l[pos+length/3]
		start   =l[pos +2*length/3]
		if start not in d.keys():
			d[float(start)]=[speaker,duration]
	
	return d

if __name__=="__main__":
	
	m=filterout()
	print "start time  :    speaker id     : duration "
	for ele in sorted(m):
		print '{:>13}'.format(str(ele))+'{:>14}'.format(m[ele][0].strip())+'{:>25}'.format(m[ele][1])

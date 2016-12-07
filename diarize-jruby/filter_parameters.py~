f=open('filtered.log','r')
d={}
l=[lines for lines in f.readlines()]
length=len(l)


def filterout():
	for pos in xrange(0,length/3):
		speaker =l[pos]
		duration=l[pos+length/3]
		start   =l[pos +2*length/3]
		if start not in d.keys():
			d[float(start)]=[speaker,duration]
	
	return sorted(d)

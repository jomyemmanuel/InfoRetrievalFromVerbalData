import os

def join(base,d,user,fname,listofspeakers):
	cur = base + '/media/' + user 
	file = open(cur + '/' + fname[6:-4] + '_full.txt','w')
	indexcount=dict()
	for x in listofspeakers:
		indexcount[x] = 1
	for elem in sorted(d):
		print indexcount
		temp = open(cur + '/' + fname[6:-4] + '/' + d[elem][0].rstrip('\n').rstrip('"').lstrip('"') + '/' + str(indexcount[d[elem][0].rstrip('\n').rstrip('"').lstrip('"')]) + '.txt','r')
		indexcount[d[elem][0].rstrip('\n').rstrip('"').lstrip('"')] = indexcount[d[elem][0].rstrip('\n').rstrip('"').lstrip('"')] + 1
		speech = d[elem][0].rstrip('\n').rstrip('"').lstrip('"') + ":" + temp.read() + "\n"
		file.write(speech)
		temp.close()
	file.close()




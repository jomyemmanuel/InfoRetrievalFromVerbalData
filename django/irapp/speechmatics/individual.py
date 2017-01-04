import os

def inditrans(base,d,user,fname,listofspeakers,api_id,api_token,lang):
	cur = base + '/media/' + user + '/' + fname[6:-4]
	indexcount = dict()
	for x in listofspeakers:
		indexcount[x] = 1
	print os.getcwd()
	for elem in sorted(d):
		os.system("python " + os.getcwd() + "/irapp/speechmatics/speechmatics.py -f " + cur + '/' + d[elem][0].rstrip('\n').rstrip('"').lstrip('"') + '/' + str(indexcount[d[elem][0].rstrip('\n').rstrip('"').lstrip('"')]) + fname[-4:] + " -l " + lang + " -i " + api_id + " -t " + api_token + " -x -o " + cur + '/' + d[elem][0].rstrip('\n').rstrip('"').lstrip('"') + '/' + str(indexcount[d[elem][0].rstrip('\n').rstrip('"').lstrip('"')]) + '.txt')
		indexcount[d[elem][0].rstrip('\n').rstrip('"').lstrip('"')] = indexcount[d[elem][0].rstrip('\n').rstrip('"').lstrip('"')] + 1
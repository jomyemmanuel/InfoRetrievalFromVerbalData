#### -----------ALL IMPORTS AND DEPENDENCIES-------------- 
import warnings

warnings.filterwarnings("ignore")

from pydub import AudioSegment
from filter_parameters import filterout
import os

####---------Relative Path setting

base = os.path.dirname(__file__)


username = raw_input("User name:")

####---------Inputting the audio file-------------

inp = raw_input("Audio Title:")
os.system('mkdir ' + base + 'UserFiles/' + username + '/' + inp[:-4])
voice = None

if(inp[-3:] == "wav"):
	voice = AudioSegment.from_wav(base + 'UserFiles/' + username + '/' + inp)
elif(inp[-3:] == "mp3"):
	voice = AudioSegment.from_mp3(base + 'UserFiles/' + username + '/' + inp)

d = filterout()

#####------- A UNIQUE LIST OF SPEAKER IDs---------
listofspeakers = list()

for elem in sorted(d):
	listofspeakers.append(d[elem][0].rstrip('\n').rstrip('"').lstrip('"'))
	#print elem,d[elem][0],d[elem][1]

listofspeakers = list(set(listofspeakers))

####--------- Folder division for user-----------

indexcount=dict()

for x in listofspeakers:
	os.system('mkdir ' + base + 'UserFiles/' + username + '/' + inp[:-4] + '/' +x)
	indexcount[x] = 1


####----------Audio Splitting and Populating the folders of the user----------

for elem in sorted(d):
	start = round(elem*1000,0)
 	duration = round(float(d[elem][1])*1000,0)
 	end = start + duration
 	part = voice[start:end]
 	part.export(base + 'UserFiles/' + username + '/' + inp[:-4] + '/' + d[elem][0].rstrip('\n').rstrip('"').lstrip('"') + '/' + str(indexcount[d[elem][0].rstrip('\n').rstrip('"').lstrip('"')]) + '.wav', format="wav")
 	indexcount[d[elem][0].rstrip('\n').rstrip('"').lstrip('"')] = indexcount[d[elem][0].rstrip('\n').rstrip('"').lstrip('"')] + 1
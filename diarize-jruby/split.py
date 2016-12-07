import warnings

warnings.filterwarnings("ignore")

from pydub import AudioSegment
from filter_parameters import filterout

#Inputting the audio file

inp = raw_input("Audio Title:")
voice = None

if(inp[-3:] == "wav"):
	voice = AudioSegment.from_wav(inp)
elif(inp[-3:] == "mp3"):
	voice = AudioSegment.from_mp3(inp)

d = filterout()

for elem in sorted(d):
	print elem,d[elem][0],d[elem][1]
# start=input("Start Time:")
# start=round(start*1000,0)
# duration=input("Duration of Speech:")
# duration=round(duration*1000,0)
# end=start+duration
# part=voice[start:end]
# part.export("out.wav", format="wav")
import warnings

warnings.filterwarnings("ignore")

from pydub import AudioSegment

#Inputting the audio file

inp =raw_input("Audio Title:")
voice=None

if(inp[-3:]=="wav"):
	voice = AudioSegment.from_wav(inp)
elif(inp[-3:]=="mp3"):
	voice = AudioSegment.from_mp3(inp)
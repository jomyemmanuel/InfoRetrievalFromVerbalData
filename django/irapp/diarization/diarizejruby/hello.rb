

# Ruby program to diarize inputed audio file . 
# Output : contains text_output  with @speaker_id @duration @start parameters  

output = File.open( "outputfile.log", "w" )
require 'diarize'
audio = Diarize::Audio.new URI ('file:///media/jake/WORK/mainproject/work/diarize-jruby/d.wav')
audio.analyze!
output << audio.segments
output.close  
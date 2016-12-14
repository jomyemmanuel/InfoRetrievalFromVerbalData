

# Ruby program to diarize inputed audio file . 
# Output : contains text_output  with @speaker_id @duration @start parameters  

puts ARGV
output = File.open( "outputfile.log", "w" )
require 'diarize'
audio = Diarize::Audio.new URI (''+ARGV[0])

audio.analyze!
output << audio.segments
output.close  
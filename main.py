import os
from diarization.diarizejruby import filter_parameters 
from splitting.split import split

####---------Relative Path setting-----------
base_dir = os.getcwd()
d=filter_parameters.filterout(os.getcwd()+'/diarization/diarizejruby/'+'filtered.log')



split(base_dir,d)



<<<<<<< HEAD
# InfoRetrievalFromVerbalData <br>
<b> Steps For Installation </b> <br>
1. virtualenv . <br>
2. source bin/activate <br>
3. pip install django <br>
4. cd django <br>
5. python manage.py makemigrations <br>
6. python manage.py migrate <br>
7. python manage.py runserver
=======
# InfoRetrievalFromVerbalData - AMAL

Hereafter everything will be referred to with below folder as base

```
1)The Base folder / absolute path root =      InfoRetrievalFromVerbalData
2)User media files folder - UserFiles
3)The main entry point will be 'main.py' which will be made to a python view to incorporate diarization and splitting into the django project.
4)If you want to create a new user for now , manually create a directory within UserFiles with the username(eg:- like ive done with the folder 'amal')
5)Put the audio file you want to diarize within this newly created user folder within UserFiles (eg:-Userfiles/amal/d.wav)
6)The rest of the folder structure is created by the split.py script i wrote  , automatically, and is self explanatory.
```

## split.py inputs 

```
*user name - same as the folder you created within UserFiles for your user
*audio file name - the name of the file you placed in this user folder to be diarized.
```
```
Then sit back , grab some pop corn and enjoy the Magic ;) 
```
>>>>>>> amal

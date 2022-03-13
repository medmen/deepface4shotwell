# deepface4shotwell

A python script for face tagging in shotwell. Face recognition is done using the [deepface](https://github.com/serengil/deepface) and [retinaface](https://github.com/serengil/retinaface) library by [serengil](https://github.com/serengil/deepface/commits?author=serengil).

Recognized faces are added to shotell's db as name tags and in addition as IPTC tags in the image itself.

Beware that face recognition using retinaface is rather slow - takes about 5sec per picture on my 10 year old corei5 processor.

Maybe i can speed that up later using parallel processing. Switching to other models should also be faster, but only retinaface 
has a built in function to extract more than one face in a picture as of now (as far as i could find out).

Feel free to improve and extend, but be gentle: this is my first python project :)

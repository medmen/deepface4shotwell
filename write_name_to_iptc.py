import logging
import pyexiv2
from pathlib import Path

# img = '/home/galak/Pictures/2017/07/09/img-20170709-wa0036.jpg'
# foundname = 'Moosmutzel'

def write_name_to_iptc(img_path, nameToWrite):
    # make sure img_path exists
    if False == Path(img_path).is_file():
        logging.WARN("cannot write iptc tag to image, it does not exist")
        return False

    # check if image path was given
    if(len(nameToWrite) < 2):
        logging.WARN("cannot write iptc tag to image, no name or name with 1 letter given")
        return False

    metadata = pyexiv2.ImageMetadata(img_path)
    metadata.read()
    if ('Xmp.iptcExt.PersonInImage' in metadata):
        tag = metadata['Xmp.iptcExt.PersonInImage']
    else:
        tag = False
    # tag = metadata['Xmp.iptcExt.PersonInImage']
    names = []
    nameexists = bool(False)

    if (tag):
        logging.info("checking if nametag %s exists", tag.value)
        names = tag.value

        for checkName in names:
            if (checkName.lower() == nameToWrite.lower()):
                nameexists = bool(True)
                logging.info("image is already tagged with %s !", checkName)
                break

    if (not nameexists):
        if (not tag):
            metadata['Xmp.iptcExt.PersonInImage'] = [nameToWrite]
            logging.info("writing new iptc tag for %s !", nameToWrite)
        else:
            names.append(nameToWrite)
            tag.value = names
            logging.info("Appending %s to existing iptc name tags !", nameToWrite)

        metadata.write()

    return True
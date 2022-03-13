# myapp.py
import logging
from deepface import DeepFace
from retinaface import RetinaFace
from deepface.basemodels import ArcFace
import pandas as pd
from imutils import paths
import cv2
import os
import write_name_to_shotwell
import write_name_to_iptc


def main():
    ### config section
    # TODO: add config parsing module
    # lets keep a log file
    logfile = 'myapp.log'

    # the directory to search for faces
    images_dir = "/home/galak/Pictures/2022"

    # path to the shotwell database
    shotwell_db = '/home/galak/.local/share/shotwell/data/photo.db'

    # a directory of "known faces" sorted by name
    # each name needs at least one image.
    # example:
    # # #
    # alice
    #       - alice1.jpg
    #       - alice2.jpg
    # bob
    #       - bob1.jpg
    # charly
    #       - charly1.jpg

    known_faces = "/opt/OpenCV/Training/"

    # a text file to keep track of images we have covered already
    known_images = 'known_images.txt'
    ### end config section

    # start logging
    log_format = (
        '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')
    # clear log file for every run, to append set filemode="a"
    logging.basicConfig(filename=logfile, filemode="w", format=log_format, level=logging.DEBUG)
    logging.info('Started')

    imagePaths = list(paths.list_images(images_dir))
    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        logging.warning("processing image {}/{}".format(i + 1, len(imagePaths)))
        print("processing image {}/{}".format(i + 1, len(imagePaths)))
        name = imagePath.split(os.path.sep)[-1]
        logging.info("image is %s in path %s", name, imagePath)

        # if image is in known_images, skip processing
        if is_known_image(known_images, imagePath):
            continue

        faces = RetinaFace.extract_faces(imagePath, align=True)
        if len(faces) == 0:
            logging.error("image %s holds no faces", name)
            add_known_image(known_images, imagePath)
            continue

        for face in faces:
            model = ArcFace.loadModel()
            df = DeepFace.find(face, db_path=known_faces, model=model, detector_backend='retinaface', enforce_detection=False)
            if df.shape[0] > 0:
                match_path = df.iloc[0].identity  # get first line of dataframe, column identity
                match = match_path.split('/')[-2]  # split path by "/", get next to last item
                logging.warning("detected %s in image", match)
                success_iptc = write_name_to_iptc.write_name_to_iptc(imagePath, match)
                success_shotwell = write_name_to_shotwell.write_name_to_shotwell(imagePath, match, shotwell_db)
                if True == success_iptc and True == success_shotwell:
                    logging.error("Match for %s found and saved successfully", match)
                    add_known_image(known_images, imagePath)
                else:
                    logging.error("Saving Data for %s failed at least partially", match)
            else:
                logging.error("image %s holds no faces", name)
                add_known_image(known_images, imagePath)

    logging.error('Finished')
    print('Finished')


def add_known_image(known_images, imagePath):
    # add to known images
    known = open(known_images, "a")
    known.write(imagePath + "\n")
    known.close()
    logging.info("adding %s to known images", imagePath)

def is_known_image(known_images, imagePath):
    try:
        known = open(known_images, "r")
        for line in known:
            if imagePath in line:
                logging.warning("file %s has been processed already, skipping", imagePath)
                return True
                break
        return False

    except (OSError, IOError, FileNotFoundError) as e:
        logging.warning("known_images is empty")
        return False

if __name__ == '__main__':
    main()
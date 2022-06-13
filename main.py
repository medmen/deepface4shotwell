#!/usr/bin/env python
import config as cfg

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
    logfile = cfg.logfile
    log_level = cfg.log_level
    images_dir = cfg.images_dir
    shotwell_db = cfg.shotwell_db
    known_faces = cfg.known_faces
    enable_testing = cfg.enable_testing
    testing_faces = cfg.testing_faces
    known_images = cfg.known_images
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
        name = imagePath.split(os.path.sep)[-1]
        logging.info("image is %s in path %s", name, imagePath)
        print("processing image {}/{} - {}".format(i + 1, len(imagePaths), name))

        # if image is in known_images, skip processing
        if is_known_image(known_images, imagePath):
            logging.info("image %s has already been processed", imagePath)
            continue

        faces = RetinaFace.extract_faces(imagePath, align=True)
        if len(faces) == 0:
            logging.error("image %s holds no faces", name)
            add_known_image(known_images, imagePath)
            continue
        print("retinaface detected {} faces !".format(len(faces)))

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
                    add_to_testing(testing_faces, face, match)
                else:
                    logging.error("Saving Data for %s failed at least partially", match)

            else:
                logging.error("image %s holds no faces", name)
                add_known_image(known_images, imagePath)

    logging.error('Finished')
    print('Finished')

def add_to_testing(testing_faces, face_img, match):
    # adds recognized images to a testing subdir for better training
    # make subdir with name if not exists
    path = os.path.join(testing_faces, match)
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)

    img_cnt = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]) + 1
    img_name = f'{match}{img_cnt}.jpg'
    target_path = os.path.join(path, img_name)
    cv2.imwrite(target_path,cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR))

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
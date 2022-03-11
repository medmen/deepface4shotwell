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
    # config section
    logfile='myapp.log'
    images_dir="/home/galak/Pictures/2022"
    shotwell_db='/home/galak/.local/share/shotwell/data/photo.db'
    known_images = 'known_images.txt'
    ####

    # start logging
    log_format = (
        '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')

    logging.basicConfig(filename=logfile, format=log_format, level=logging.WARNING)
    logging.info('Started')

    imagePaths = list(paths.list_images(images_dir))
    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        logging.warning("processing image {}/{}".format(i + 1, len(imagePaths)))
        name = imagePath.split(os.path.sep)[-1]
        logging.info("image is %s in path %s", name, imagePath)

        faces = RetinaFace.extract_faces(imagePath, align=True)
        for face in faces:
            model = ArcFace.loadModel()
            df = DeepFace.find(face, db_path="/opt/OpenCV/Training/",
                               model=model, detector_backend='retinaface', enforce_detection=False)
            if df.shape[0] > 0:
                match_path = df.iloc[0].identity  # get first line of dataframe, column identity
                match = match_path.split('/')[-2]  # split path by "/", get next to last item
                logging.warning("detected %s in image", match)
                success_iptc = write_name_to_iptc.write_name_to_iptc(imagePath, match)
                success_shotwell = write_name_to_shotwell.write_name_to_shotwell(imagePath, match, shotwell_db)
                if True == success_iptc and True == success_shotwell:
                    logging.error("Match for %s found and saved successfully", match)
                else:
                    logging.error("Saving Data for %s failed at least partially", match)

    logging.ERROR('Finished')

if __name__ == '__main__':
    main()
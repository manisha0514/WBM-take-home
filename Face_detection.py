'''This script uses OpenCV's haarcascade to detect faces in a given input image.'''

# Import necessary libraries
import os
import cv2 as cv
import logging


def main():
    # variables for Input and output directories
    input_path = os.path.dirname(os.path.abspath(__file__)) + "\Input"
    output_path = os.path.dirname(os.path.abspath(__file__)) + "\FaceImages"
    haarcascase_xml = os.path.dirname(os.path.abspath(__file__)) + "\Haarcascade\haarcascade_frontalface_default.xml"

    # Load face cascade from haarcascades folder
    if os.path.isfile(haarcascase_xml):
        face_cascade = cv.CascadeClassifier(haarcascase_xml)

        # Read image in img and convert it to grayscale and store in gray.
        image_files = os.listdir(input_path)
        for file in image_files:
            # Included JPEG, JPG, PNG formats
            if file.endswith(('jpg', 'png', 'jpeg')):
                try:
                    img = cv.imread(input_path + "/" + file)
                    if img.shape != None:
                        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

                        # Detect all faces in image.
                        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                        # Draw a rectangle over the face, and detect eyes in faces
                        face_count = 0
                        for (x, y, w, h) in faces:
                            face_count += 1
                            face_filename = file + "_face_" + str(face_count) + ".jpg"

                            # ROI is region of interest with area having face inside it.
                            roi_color = img[y:y + h, x:x + w]
                            cv.imwrite(output_path + "/" + face_filename, roi_color)
                            cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                        cv.imshow('Image', img)
                        cv.waitKey(0)
                        cv.destroyAllWindows()
                        print("Total " + str(face_count) + " found in file " + file)
                    else:
                        logging.warning("Image not loaded properly")

                except Exception as e:
                    logging.error("Problem in detecting Face images" + str(e))

            else:
                logging.warning("Files should only be in JPEG, JPG, PNG Formats")
    else:
        logging.warning("Haar cascade model file not found")


if __name__ == "__main__":
    main()

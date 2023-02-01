'''This script is to check transparent pixels and move to s3 bucket if not found.'''

# Import necessary libraries
import sys
from io import BytesIO
import logging
from PIL import Image
import boto3
import botocore


def is_transparency(img):
    """check for transparency of image

        :param img: PIL image to check
        :return: True if image is transparent, else False
        """

    # if the image information has transparency parameter then return True
    if img.info.get("transparency", None) is not None:
        return True

    # if image mode is P check for transparency in image information and do the check then return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True

    # image mode is RGBA the get the extrema values and check if it is less than 255 then return true
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    # if no conditions are satisfied return false
    return False


def main(args):
    """check for transparency of image

           :param args[1]: aws access key id
           :param args[2]: aws secret access key
           :param args[3]: source bucket name
           :param args[4]: target bucket name

    """

    if len(args) < 5:
        logging.warning("Enough Command line Arguments not Found")

    else:
        aws_access_key_id = args[1]
        aws_secret_access_key = args[2]
        source_bucket_name = args[3]
        target_bucket_name = args[4]

        # providing AWS credentials to Boto3

        try:
            session = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )

            # Creating S3 client and Resource From the Session.
            s3 = session.resource('s3')
            s3_cli = session.client("s3")

            # initializing the source and target bucket names
            source_bucket = s3.Bucket(source_bucket_name)
            target_bucket = s3.Bucket(target_bucket_name)

            if len(list(source_bucket.objects.all())) > 0:
                # List all files from source bucket and iterate to check for transparent pixels
                files_copied = 0
                files_not_copied = 0
                for source_bucket_object in source_bucket.objects.all():
                    print(source_bucket_object.key)
                    # Get image from bucket and read using PIL
                    new_obj = s3_cli.get_object(Bucket=source_bucket.name, Key=source_bucket_object.key)
                    image_dl = new_obj['Body'].read()
                    image = Image.open(BytesIO(image_dl))

                    # transparency check
                    if len(image.size) == 2:
                        if not is_transparency(image):
                            # if not transparent copy to another s3 bucket

                            copy_source = {
                                'Bucket': source_bucket.name,
                                'Key': source_bucket_object.key
                            }
                            try:

                                s3_cli.copy_object(
                                    Bucket=target_bucket.name,
                                    Key=source_bucket_object.key,
                                    CopySource=copy_source
                                )
                                print(source_bucket_object.key + 'Image is copied to ' + target_bucket.name)
                                files_copied +=1
                            except Exception as e:
                                logging.error("Issue in moving file to another bucket "+str(e))

                        else:
                            # if transparent log into text file
                            try:
                                with open("transparent_image_log.txt", "a") as f:
                                    f.write(source_bucket_object.key + '\n')
                                    files_not_copied +=1
                            except Exception as e:
                                logging.error("Error while writing into transparent log File")
                    else:
                        logging.error("Problem in loading the image")
            else:
                logging.warning("No Images in the s3 Bucket")

        except Exception as e:
            logging.warning(" wrong aws access credentials provided"+str(e))

    print("Total Images", len(list(source_bucket.objects.all())) )
    print("Non transparent Images ", files_copied)
    print("Total transparent Images", files_not_copied)
if __name__ == "__main__":
    main(sys.argv)

# WBM-take-home
## Face Detection
Detecting faces from the images with group of people
### Files for Face Detection
 1. Input - copy all the input images to this path for detecting the face images
 2. haarcascae - model file for face detection algorithm
 3. Face Images - output path for saving the headshots of the detected faces 
 
 Output:
 ###### Total 5 faces found in file istockphoto-1344872631-170667a.jpg
 
### Run Command
#### python Face_detection.py

## check transparent pixels
1. check the transparent images and write log files for it if not transparent copy to another s3 bucket
2. to run this file all the 4 arguments are required aws_access-id, aws-access-key, source bucket, dest bucket
3. sample policy.json file for s3 bucket permissions

Output:
###### Total Images 6
###### Non transparent Images  4
###### Total transparent Images 2

### Run Command
#### python check_transparency.py AKIAIOSFODNN7EXAMPLE wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY src-bucket-name dest-bucket-name
given access crendtials are samples taken from aws site

  

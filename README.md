#follow the steps in "instructions for setup" to prepare python and flask environments.


After setting up the environment run the app using command: flask run  
By default the app runs on port 5000 but the address can be changed from the file run.py


A new session for the app can be started from the sign in page or sign up page, (for login is username is “user” and password is “password”,   this creates a new folder for file upload and download that include session ID and the timestamp and the folder is used for the entire run of the session).


After signing in, the page redirects to two image editing tools page which is divided into two sections, basic and advanced tools
Basic tools are:
    1. Convert png to jpg
    2. Reshape image
    3. Trim image
    4. Art frame  margins or border to image
    5. Resize image
Advance tools are:
    1. Watermark
    2. Make a combo of images


Each of the above tool redirect to a new page dealing with the respective tool, 

Convert png to jpg : /convert-Png-To-Jpg
    *Upload image Into the upload box,  single image at a time
    *Click on upload button to upload the image and then the convert button for conversion and compression of image, the result can be downloaded from the “download” button.
    *The image is optimised and converted to a JPG but the file name is preserved.


Reshape Image: /reshape-image 
    *Upload image Into the upload box,  single image at a time
    *Choose a type for conversion:
        1. Simple:  directly converts the image to a square
        2. Advanced: Margin can be added as percentage over object size, You can also specify the aspect ratio for image and the image can be reshaped into any size.
        result can be downloaded by clicking on download button, the filename is preserved
    *Click on the download button to download the result


Trim Image: /trim-image
    *Upload image Into the upload box,  single image at a time
    *Click on the trim button to begin trimming, all excess white background margins are border are been removed from the image and only the object is left
    (Sometimes this may not work for object pictures which have  large white areas in the middle or for some peculiar diagonal shapes which may not be recognised as object box in a rectangle algorithm)
    *Click on the download button for downloading the result,  it downloads the trimmed image and preserves the filename


Add margins or border: /add-margin
    *Upload image Into the upload box,  single image at a time 
    *Margins can be added as percentage over image size or it can be input in pixels
    *Click on the add margin button to start processing
    *Click on the download button to  download the result image


Resize Image: /resize-image
    *Upload image Into the upload box,  single image at a time 
    *Resize the image giving sizing as percentage of original for specified dimensions in pixels click on resize image button for resizing the image
    *Click on download button for downloading the result image 


Watermark: /watermark-on-image
    Upload image Into the upload box,  single image at a time 
    Watermark and report on your image with the variety of options: 
    * Input a text for water mark which is to be written on the image
    * Choose a font for your watermark text from Arial, Impact and Verdana
    * Choose a font size for watermark, sizes to be given in pixel
    * Choose a colour for watermark and a level for transparency
    * finally selected position reference  as any of the four corners or at the centre
    Click on add watermark button  to start processing
    Click on download button to get the Resultant image 


Create Combo: /create-combo
    Upload image Into the upload box, multi-file upload
    Combo of images can be created with a variety of options and customizations:
    * Choose the combo type preference,  and whether it should contain multiple images or same image should be repeated 
    * Linear combo has the following options: Number of repetitions can be input, Overlap percentage for images and direction choice from horizontal or vertical
    * Grid combos has the following options: Grid size can be specified as number of images on height and width dimensions,  for instance  on input of 6 images a grid size of 2 x 3

Apart from these, each page has a navbar, with options for redirecting to the tools page and an option for signing-out and ending the current session. 

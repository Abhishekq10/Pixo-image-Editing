import uuid
import os
from flask import Flask, render_template, send_from_directory, abort, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import cv2
from app import app
from lib import convert, reshape_tools, dir_maker, watermark, combo_tools

app.config["IMAGE_UPLOADS"] = "/home/site/wwwroot/App/app/static/img/uploads" 
#full path to uploads folder
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
#specify max file size in bytes
app.config["CLIENT_IMAGES"] = "/home/site/wwwroot/App/app/static/img/down"
#full path to download folder
app.config["SECRET_KEY"] = "liruhfoi34uhfo8734yot8234h"


def allowed_image(filename):
    '''function to check file extension
    a file without extension might be a system executable'''
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


def uploader_with_file_name(req):
    if req.method == "POST":
        if req.files:
            image = req.files["image"]
            if image.filename == "":
                print("No filename")
                return redirect(req.url)
            if allowed_image(image.filename):
                app.config["filename"] = secure_filename(image.filename)
                image.save(os.path.join(
                    app.config["IMAGE_UPLOADS"], app.config["filename"]))
                print("Image uploaded")
                return redirect(request.url)
            else:
                print("That file extension is not allowed")
                return redirect(req.url)


@app.route('/', methods=["GET", "POST"])
def index():
    '''render index page with tools'''
    return render_template("public/index.html")

@app.route("/get-image/<image_name>", methods=["GET", "POST"])
def get_image(image_name):
    '''download image specified as query
    file name is specified, path is set to current session's download folder
    '''
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], filename=image_name,
                                   as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/get-img", methods=["GET", "POST"])
def get_img():
    '''download image from current session's download folder
    file name is taken from the app constant app.config["filename"]
    '''
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], 
                                    filename=app.config["filename"], as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route("/convert-Png-To-Jpg", methods=["GET", "POST"])
def uploader_for_convert():
    '''upload single file for conversion and compression'''
    uploader_with_file_name(request)
    return render_template("public/convertPngToJpg.html")


@app.route("/converter", methods=["GET", "POST"])
def converter():
    '''convert image to JPG and also optimize image using PIL'''
    if request.method == "POST":
        in_image = app.config["IMAGE_UPLOADS"]+"/"+app.config["filename"]
        out_image = app.config["CLIENT_IMAGES"]+"/"
        print(app.config["filename"])
        name, ext = os.path.splitext(app.config["filename"])
        app.config["filename"] = name+".jpg"
        print("new name")
        print(app.config["filename"])
        convert.convertPngToJpg(in_image, out_image)
    return render_template("public/convertPngToJpg.html")

@app.route('/reshape-image', methods=["GET", "POST"])
def uploader_for_reshape():
    '''upload single image for reshaping'''
    uploader_with_file_name(request)
    return render_template("public/reshape-image.html")


@app.route('/reshaping', methods=["GET", "POST"])
def reshaping_image():
    '''collect form data and reshape image as per'''
    if request.method == "POST":
        req = request.form
        margin = int(req.get("marginPer"))
        aspectWidth = int(req.get("aspectWidth"))
        aspectHeight = int(req.get("aspectHeight"))
        in_image = app.config["IMAGE_UPLOADS"]+"/"+app.config["filename"]
        out_image = app.config["CLIENT_IMAGES"]+"/"+app.config["filename"]
        reshape_tools.reshape_Image(in_image, out_image, 1,
                                    aspectRatio=(aspectWidth, aspectHeight), percentageMargin=margin)
    return redirect(url_for("uploader_for_reshape"))


@app.route('/add-margin', methods=["GET", "POST"])
def uploader_for_margin():
    '''upload single image for adding margin'''
    uploader_with_file_name(request)
    return render_template("public/add-margin.html")


@app.route('/margins', methods=["GET", "POST"])
def add_margin():
    '''collect form data and add margins as per'''
    if request.method == "POST":
        req = request.form
        marginPer = int(req.get("marginPer"))
        marginPix = int(req.get("marginPix"))
        in_image = app.config["IMAGE_UPLOADS"]+"/"+app.config["filename"]
        out_image = app.config["CLIENT_IMAGES"]+"/"+app.config["filename"]
        reshape_tools.addMargins(in_image, out_image, percentageMargin=marginPer,
                                 marginPixels=marginPix)
    return redirect(url_for("uploader_for_margin"))


@app.route("/resize-image", methods=["GET", "POST"])
def uploader_for_resize():
    '''upload single image for resizing'''
    uploader_with_file_name(request)
    return render_template("public/resize-image.html")


@app.route("/resizing", methods=["Get", "POST"])
def resizing():
    '''collect form data and resize image as per'''
    if request.method == "POST":
        req = request.form
        scalePer = int(req.get("scalePer"))
        imgHeight = int(req.get("imgHeight"))
        imgWidth = int(req.get("imgWidth"))
        in_image = app.config["IMAGE_UPLOADS"]+"/"+app.config["filename"]
        out_image = app.config["CLIENT_IMAGES"]+"/"+app.config["filename"]
        reshape_tools.resizeImage(
            in_image, out_image, scalePer, (imgWidth, imgHeight))
    return redirect(url_for("uploader_for_resize"))


@app.route("/trim-image", methods=["GET", "POST"])
def uploader_for_trim():
    '''upload single image for trimming'''
    uploader_with_file_name(request)
    return render_template("public/trim-object.html")


@app.route("/trimming", methods=["GET", "POST"])
def trimming():
    '''trim image to object'''
    if request.method == "POST":
        in_image = app.config["IMAGE_UPLOADS"]+"/"+app.config["filename"]
        out_image = app.config["CLIENT_IMAGES"]+"/"+app.config["filename"]
        image = cv2.imread(in_image)
        image = reshape_tools.trim(image)
        cv2.imwrite(out_image, image)

    return redirect(url_for("uploader_for_trim"))


@app.route("/watermark-on-image", methods=["GET", "POST"])
def uploader_for_watermark():
    '''upload single image for putting watermark'''
    uploader_with_file_name(request)
    return render_template("public/watermark.html")


@app.route("/put-watermark", methods=["GET", "POST"])
def putWatermark():
    '''collect form data and put watermark on image'''
    if request.method == "POST":
        req = request.form
        fontFace = req.get("fontFace")
        fontSize = int(req.get("fontSize"))
        text = req.get("watermarkText")
        markPosition = req.get("watermarkPosition")
        markColor = req.get("watermarkColor")
        markColor = watermark.hex_to_rgb(markColor)
        opacity = int(req.get("watermarkOpacity"))
        in_image = app.config["IMAGE_UPLOADS"]+"/"+app.config["filename"]
        out_image = app.config["CLIENT_IMAGES"]+"/"+app.config["filename"]

        watermark.watermarker(in_image, out_image, text, fontFace, fontSize,
                              markColor, opacity, position=markPosition)
    return redirect(url_for("uploader_for_watermark"))


@app.route("/create-combo", methods=["GET", "POST"])
def uploader_for_combo():
    '''multiple file upload for making combo'''
    if request.method == "POST":
        if request.files:
            for image in request.files.getlist('image'):
                if image.filename == "":
                    print("No filename")
                    return redirect(request.url)
                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(
                        app.config["IMAGE_UPLOADS"], filename))
                    print("Image saved")
                else:
                    print("That file extension is not allowed")
                    return redirect(request.url)
            return redirect(request.url)
    return render_template("public/comboMaker.html")


@app.route("/combining", methods=["GET", "POST"])
def createCombo():
    '''collect data from for and make combo'''
    if request.method == "POST":
        req = request.form
        in_path = app.config["IMAGE_UPLOADS"]
        out_path = app.config["CLIENT_IMAGES"]+"/"
        comboType = req.get("comboType")
        repeatImage = bool(req.get("repeatImage"))
        repeatCount = int(req.get("repeatCount"))
        overlap = int(req.get("overlap"))
        direction = (req.get("direction"))
        gridHeight = int(req.get("gridHeight"))
        gridWidth = int(req.get("gridWidth"))
        combo_tools.createCombo(in_path, out_path, comboType, overlap, direction,
                                repeatImage, repeatCount, gridHeight, gridWidth)
    return redirect(url_for("uploader_for_combo"))


users = {
    "admin": {
        "username": "admin",
        "email": "boss@gmail.com",
        "password": "imtheboss",
        "bio": "meh"
    },
    "user": {
        "username": "user",
        "email": "user@icloud.com",
        "password": "password",
        "bio": "chocolates are the best"
    }
}


@app.route('/sign-in', methods=["GET", "POST"])
def sign_in():
    '''log in the user for usage session usage
        check for the login data from a dictionary
        can be replaced with a reference check from any database

        > create a session folder for upload and download
        > set these as as location for running sessions
        > redirect to tools page  
    '''
    if request.method == "POST":
        req = request.form
        username = req.get("username")
        password = req.get("password")

        if not username in users:
            print("Username not found")
            return redirect(request.url)
        else:
            user = users[username]

        if not password == user["password"]:
            print("Incorrect password")
            return redirect(request.url)
        else:
            session["USERNAME"] = user["username"]
            session['uid'] = uuid.uuid4()
            print("session username set")
            print(session)
            uid = session.get("uid")
            upload_path = dir_maker.create_dir_with_uid(
                app.config["IMAGE_UPLOADS"], str(uid))
            app.config["IMAGE_UPLOADS"] = upload_path
            download_path = dir_maker.create_dir_with_uid(
                app.config["CLIENT_IMAGES"], str(uid))
            app.config["CLIENT_IMAGES"] = download_path
            return redirect(url_for("index"))
    return render_template("public/sign_in.html")


@app.route("/profile")
def profile():
    '''render a user profile page for current user'''
    if session.get("USERNAME", None) is not None:
        username = session.get("USERNAME")
        user = users[username]
        return render_template("public/profile.html", user=user)
    else:
        print("Username not found in session")
        return redirect(url_for("sign_in"))


@app.route("/sign-out")
def sign_out():
    '''clear data from session'''
    session.pop("USERNAME", None)
    session.pop("uid", None)

    return redirect(url_for("sign_in"))

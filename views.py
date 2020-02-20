__author__ = 'Yash'

from io import BytesIO
from flask_uploads import UploadSet, IMAGES,configure_uploads
from flask import render_template,send_file
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from app import app
from PIL import Image

#.jpg, .jpe, .jpeg, .png, .gif, and .bmp are allowed image extensions according to the Uploadset IMAGES
images = UploadSet('images', IMAGES)
configure_uploads(app, (images))

class PhotoForm(FlaskForm):
    """[Class that handle the form layout and input image to be taken from the user]
    
    Arguments:
        FlaskForm {[Flask-WTF Object]} -- [Using the base template provided by Flask WTF-Forms]
    """
    photo = FileField(validators=[FileRequired(), FileAllowed(images, 'Images only!')])

@app.route('/',methods=['GET','POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        photo_data = form.photo.data
        mime_type, image_format = get_mimetype_format(photo_data)
        square_image = get_resized_image(photo_data)
        buffer = BytesIO()
        square_image.save(buffer, image_format, quality=70)
        buffer.seek(0)
        return send_file(buffer, mimetype=mime_type)

    return render_template('index.html', form=form)

def get_mimetype_format(photo_data):
    """[Get Mimetype and format of the image from the image uploaded]
    
    Arguments:
        photo_data {[Object]} -- [Photo data of the image uploaded]
    
    Returns:
        [String] -- [Mimetype of the image]
        [String] -- [Format of the image]
    """
    mime_type = photo_data.mimetype
    image_format = mime_type.split('/')[1]
    return mime_type, image_format
    
def get_resized_image(photo_data):
    """[Get new image that is square in dimesnions]
    
    Arguments:
        photo_data {[Object]} -- [Photo data of the image uploaded]
    
    Returns:
        [Object] -- [Photo data of the new image that is square in dimensions]
    """
    photo_stream_data = BytesIO(photo_data.stream.read())
    image_to_process = Image.open(photo_stream_data)
    width,height = image_to_process.size
    new_size = width
    if height < width:
        new_size = height

    square_image = image_to_process.resize((new_size,new_size))
    return square_image


if __name__ == "__main__":
    app.run()


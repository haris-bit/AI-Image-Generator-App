from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI  # Make sure to import OpenAI
from PIL import Image
import io
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os


# initialize the Flask app and the OpenAI client
app = Flask(__name__)
client = OpenAI()  # Initialize the OpenAI client


app.config["SECRET_KEY"] = "andrewgreen"
app.config["UPLOAD_FOLDER"] = "static/files"



class UploadFileForm(FlaskForm):
    file = FileField("file")
    submit = SubmitField("Upload File")






@app.route('/')
def index():
    return render_template('form.html')  # Render the form template

@app.route('/test', methods=["GET", "POST"])
def test():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        filename = secure_filename(file.filename) # Then secure the filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', filename=filename, form=form)
    return render_template('index.html', form=form)


@app.route('/submit', methods=['POST'])
def handle_form_submission():
    prompt = request.form['prompt']




    try:
        # Use the working code from sample.py for image generation
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # Extract the image URL from the response
        image_url = response.data[0].url
        name = "Andrew Green"
        
        # Render the template to display the image
        if "logo" in request.files:
            logo_file = request.files['logo']
            if logo_file:
                background = Image.open(image_url)
                logo = Image.opeb(logo_file.stream).convert("RGBA")

                logo_size = (100, 100)

                logo.thumbnail(logo_size, Image.ANTIALIAS)

                position = (background.width - logo.width, background.height - logo.height)

                background.paste(logo, position, logo)

                img_io = io.BytesIO()
                background.save(img_io, 'PNG', quality=100)
                img_io.seek(0)
                return send_file(img_io, mimetype='image/png')


        return render_template('display_image.html', image_url=image_url, name=name)

    except Exception as e:
        # Return a JSON response if an error occurs
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

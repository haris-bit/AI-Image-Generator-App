from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI  # Make sure to import OpenAI
from PIL import Image
import io
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from flask import session


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



@app.route('/submit', methods=["GET", "POST"])
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
        image_url = str(response.data[0].url)


        # Store the image URL in the session
        session['image_url'] = image_url
        
            
        
        form = UploadFileForm()
        if form.validate_on_submit():
            file = form.file.data # First grab the file
            filename = secure_filename(file.filename) # Then secure the filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('display_image.html', image_url=image_url, filename=filename, form=form)
        


        return render_template('display_image.html', image_url=image_url, form=form)

    except Exception as e:
        # Return a JSON response if an error occurs
        return jsonify({'error': str(e)}), 500


@app.route('/success', methods=["GET", "POST"])
def testing():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        filename = secure_filename(file.filename) # Then secure the filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Retrieve the image URL from the session
        image_url = session.get('image_url')
        return render_template('display_image.html', filename=filename, form=form, image_url=image_url)
    return render_template('display_image.html', form=form)






if __name__ == '__main__':
    app.run(debug=True)

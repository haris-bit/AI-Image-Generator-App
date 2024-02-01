from flask import Flask, render_template, request, jsonify
from openai import OpenAI  # Make sure to import OpenAI

# initialize the Flask app and the OpenAI client
app = Flask(__name__)
client = OpenAI()  # Initialize the OpenAI client

@app.route('/')
def index():
    return render_template('form.html')  # Render the form template

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
        return render_template('display_image.html', image_url=image_url, name=name)

    except Exception as e:
        # Return a JSON response if an error occurs
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

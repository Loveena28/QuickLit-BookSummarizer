from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from google.cloud import vision
import os, openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(
    __name__, static_url_path="", static_folder="static", template_folder="templates"
)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, supports_credentials=True)
openai.api_key = os.environ.get("API_KEY")


# Set up Google Cloud Vision API credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "pharma-growth-330207-554096c10156.json"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ocr", methods=["POST"])
def ocr():
    # Check if the POST request has a file part
    if "image" not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files["image"]

    # Check if the file is empty
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    # Read the image file into memory
    image_content = file.read()

    # Initialize the Cloud Vision API client
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=image_content)
    features = [vision.Feature(type_=vision.Feature.Type.TEXT_DETECTION)]

    # Detect the text in the image
    vision_request = vision.AnnotateImageRequest(image=image, features=features)
    vision_response = client.annotate_image(request=vision_request)

    # Extract the book title from the detected text
    for annotation in vision_response.text_annotations:
        title = annotation.description
        break

    model_engine = "gpt-3.5-turbo-instruct"
    prompt = (
        "write summary for the book "
        + title
        + " and return the summary, title and author in strictly json format with keys title, author, summary just like this example : {title:,author:,summary:}"
    )

    # Generate a response
    completion = openai.completions.create(
        model=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    ai_response = completion.choices[0].text

    # Return the extracted text as JSON
    return ai_response


if __name__ == "__main__":
    app.run()

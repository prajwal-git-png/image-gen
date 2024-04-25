import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class StabilityAI:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer sk-n7A79xf4jkfhsfD8pBS0uSyU2YvKiATgl9W6hRMN6eIYZMuZ"
        }

    def text_to_image(self, text):
        description_body = {"text_prompts": [{"text": text}]}
        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image", 
            # "https://api.stability.ai/v2beta/stable-image/generate/sd3",
            json=description_body, headers=self.headers)
        json_response = response.json()
        if "message" in json_response:    
            raise Exception(json_response["message"])
        result = json_response["artifacts"][0]["base64"]
        return "data:image/png;base64," + result

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.json["text"]
        stability_ai = StabilityAI()
        image_src = stability_ai.text_to_image(user_input)
        return jsonify({"image_src": image_src})
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=8080)

import os
import requests
from flask import Flask, request, render_template, flash, redirect, url_for
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/images"
app.secret_key = "testsecretkey"


def scrape_images(search_query, num_images):
    folder_path = os.path.join(app.config["UPLOAD_FOLDER"], search_query)
    os.makedirs(folder_path, exist_ok=True)

    url = f"https://www.google.com/search?q={search_query}&tbm=isch&num={num_images+1}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    image_tags = soup.find_all("img")
    for i, img_tag in enumerate(image_tags[1 : num_images + 1]):
        img_url = img_tag.get("src")
        img_data = requests.get(img_url).content
        with open(os.path.join(folder_path, f"image_{i+1}.png"), "wb") as f:
            f.write(img_data)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search_query = request.form["search_query"]
        num_images = int(request.form["num_images"])
        scrape_images(search_query, num_images)

        flash(f'Images for "{search_query}" have been downloaded.')

        return redirect(url_for("index"))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

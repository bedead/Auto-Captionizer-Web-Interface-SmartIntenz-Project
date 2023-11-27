from flask import Flask, render_template, request, redirect, url_for
import os
from GenerateCaption import generate_caption

app = Flask(__name__)

logged = False
admins = [
    {"username": "admin", "password": "admin"},
]


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/get_captions", methods=["GET", "POST"])
def get_captions():
    global logged

    if logged:
        if request.method == "POST":
            # Handle the uploaded image and generate caption
            image_file = request.files["image"]

            # Specify the upload folder with the correct path
            upload_folder = r"F:\Projects\FlaskICG\Upload"

            # Ensure the upload folder exists
            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(upload_folder, image_file.filename)
            image_file.save(file_path)

            # Correct variable name used for generate_caption
            caption = generate_caption(file_path)
            print(caption)
            return render_template("get_captions.html", caption=caption, logged=logged)

        return render_template("get_captions.html", logged=logged)

    else:
        return redirect(url_for("home"))


@app.route("/login", methods=["GET", "POST"])
def login():
    global logged, admins
    if logged:
        return redirect(url_for("get_captions"))
    elif request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        print(username)
        print(password)

        for each in admins:
            if (each["username"] == username) and (each["password"] == password):
                logged = True
                print("here")

        return redirect(url_for("get_captions"))
    else:
        return render_template("login.html")


@app.route("/signout", methods=["GET", "POST"])
def signout():
    global logged

    logged = False
    return redirect(url_for("home"))


if __name__ == "_main_":
    app.run(debug=True)

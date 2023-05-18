from flask import Flask, render_template, redirect, url_for, request
from repo import repository, Link
from datetime import datetime
import random
import string


app = Flask(__name__)
app.secret_key = "your_secret_key"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form.get("long_url")
        random_string = " ".join(
            random.choices(string.ascii_letters + string.digits, k=5)
        )
        link = Link(
            url=long_url, hash_id=random_string, created_at=datetime.utcnow()
        )
        repository.create(link)
        links_url = url_for("link_list")
        return redirect(links_url)
    return render_template("index.html")


@app.route("/link/list")
def link_list():
    links = repository.get()
    return render_template("link_list.html", links=links)


@app.route("/<hash_id>")
def _redirect(hash_id):
    link = repository.get(hash_id)
    if link:
        repository.update(link)
        redirect.link(link.url)


if __name__ == "__main__":
    app.run(debug=True)

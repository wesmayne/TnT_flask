from flask import Flask, render_template, url_for

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def home():
    """Landing page"""
    return render_template("/index.html", title="Track n Trace")


@app.route("/about")
def about():
    """About page"""
    return render_template("/about.html", title="TnT - About")


@app.route("/orders")
def orders():
    """Orders page"""
    return render_template("/index.html", title="TnT - Orders")


@app.route("/late")
def late():
    """Late page"""
    return render_template("/late.html", title="TnT - Late")


@app.route("/si")
def si():
    """SI page"""
    return render_template("/si.html", title="TnT - SI")


@app.route("/detail")
def detail():
    return render_template("/detail.html", title=f"TnT - {id}")


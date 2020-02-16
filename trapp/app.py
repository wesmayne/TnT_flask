from flask import Flask, render_template, url_for, redirect, request
from config import Config
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="static", template_folder="templates")

connection_string = f"mssql+pymssql://{Config.user}:{Config.password}@{Config.servername}/{Config.database}"
engine = sqlalchemy.create_engine(connection_string)
conn = engine.connect()
query = conn.execute("SELECT * FROM [LDD.AppSheet_NO]").fetchall()


@app.route("/test", methods=["GET"])
def test():
    """testing late"""
    picked = []
    for row in query:
        if row["Status"] == "Picked":
            picked.append(row)

    return render_template("/index.html",query=picked)


@app.route("/", methods=["GET"])
def home():
    """Landing page"""
    return redirect(url_for("orders"))


@app.route("/about", methods=["GET"])
def about():
    """About page"""
    return render_template("/about.html", title="TnT - About")


@app.route("/status", methods=["GET"])
def status():
    """System Status page"""
    return render_template("/status.html", title="TnT - Status")


@app.route("/orders", methods=["GET"])
def orders():
    """Orders page"""
    return render_template("/index.html", title="TnT - Orders", query=query)


@app.route("/late", methods=["GET"])
def late():
    """Late page"""
    late = []
    for row in query:
        if row["Status"] == "LATE":
            late.append(row)
    return render_template("/index.html", title="TnT - Late", query=late)


@app.route("/si", methods=["GET"])
def si():
    """SI page"""
    si = []
    for row in query:
        if row["SICode"] is not None:
            si.append(row)
    return render_template("/index.html", title="TnT - SI", query=si)


# need help with the search function
@app.route("/search")
def search():
    """Search page"""
    return render_template("/index.html", title="TnT - Search", query=query)


@app.route("/orders/<order>")
def detail(order):
    detail = []
    for row in query:
        if row['OrderNumber'] == order:
            detail.append(row)

    site = detail[0][2]
    status = detail[0][7]
    order = detail[0][1]
    address = detail[0][4]
    suburb = detail[0][5]
    state = detail[0][6]
    delivery_time = detail[0][9]
    cus_window = detail[0][10]
    signed_by = detail[0][12]
    to_window = detail[0][14]
    del_instructions = detail[0][13]
    si_code = detail[0][16]
    tnt_url = detail[0][18]
    attachment1 = detail[0][19]
    attachment2 = detail[0][20]
    attachment3 = detail[0][21]
    attachment4 = detail[0][22]

    return render_template(
        "/detail.html",
        title="TnT - Detail",
        site=site,
        order=order,
        status=status,
        address=address,
        suburb=suburb,
        state=state,
        delivery_time=delivery_time,
        cus_window=cus_window,
        signed_by=signed_by,
        to_window=to_window,
        del_instructions=del_instructions,
        si_code=si_code,
        tnt_url=tnt_url,
        attachment1=attachment1,
        attachment2=attachment2,
        attachment3=attachment3,
        attachment4=attachment4,
    )


if __name__ == "__main__":
    app.run(debug=False)

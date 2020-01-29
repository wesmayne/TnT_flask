from flask import Flask, render_template, url_for, redirect
from config import Config
import sqlalchemy

app = Flask(__name__, static_folder="static", template_folder="templates")


connection_string = f"mssql+pymssql://{Config.user}:{Config.password}@{Config.servername}/{Config.database}"
engine = sqlalchemy.create_engine(connection_string)
conn = engine.connect()


@app.route("/", methods=["GET"])
def home():
    """Landing page"""
    return redirect(url_for("orders"))


@app.route("/about", methods=["GET"])
def about():
    """About page"""
    return render_template("/about.html", title="TnT - About")


@app.route("/orders", methods=["GET"])
def orders():
    """Orders page"""
    query = conn.execute("SELECT * FROM [LDD.AppSheet_NO]")
    # orders = query.fetchall()
    return render_template("/index.html", title="TnT - Orders", query=query)


@app.route("/late", methods=["GET"])
def late():
    """Late page"""
    return render_template("/late.html", title="TnT - Late")


@app.route("/si", methods=["GET"])
def si():
    """SI page"""
    return render_template("/si.html", title="TnT - SI")


@app.route("/si/test", methods=["GET"])
def test():
    """SI page"""
    return render_template("/si.html", title="TnT - SI")


@app.route("/orders/<order>")
def detail(order):
    query = conn.execute(f"SELECT * FROM [LDD.AppSheet_NO] where OrderNumber = {order}")
    rows = query.fetchall()

    # vars
    site = rows[0][2]
    status = rows[0][7]
    order = rows[0][1]
    address = rows[0][4]
    suburb = rows[0][5]
    state = rows[0][6]
    delivery_time = rows[0][9]
    cus_window = rows[0][10]
    signed_by = rows[0][12]
    to_window = rows[0][14]
    del_instructions = rows[0][13]
    si_code = rows[0][16]

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
    )


if __name__ == "__main__":
    app.run(debug=True)

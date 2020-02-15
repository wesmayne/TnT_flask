from flask import Flask, render_template, url_for, redirect, request
from config import Config
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# import flask_whooshalchemy


app = Flask(__name__, static_folder="static", template_folder="templates")


connection_string = f"mssql+pymssql://{Config.user}:{Config.password}@{Config.servername}/{Config.database}"
engine = sqlalchemy.create_engine(connection_string)
conn = engine.connect()
'''
# this is where im trying to create a direct connection to the table

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mssql+pymssql://{Config.user}:{Config.password}@{Config.servername}/{Config.database}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['WHOOSH_BASE']='whoosh'

db = SQLAlchemy(app)

customer = db.Table(
    "LDD.Appsheet_NO", db.metadata, autoload=True, autoload_with=db.engine
)


@app.route("/test", methods=["GET"])
def test():
    """testing page"""
    query = db.session.query(customer).whoosh_search(request.args.get('query')).all()
    sitecode = results[0][1]
    return render_template("/index.html",query=query)
'''


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
    query = conn.execute("SELECT * FROM [LDD.AppSheet_NO]")
    return render_template("/index.html", title="TnT - Orders", query=query)


@app.route("/late", methods=["GET"])
def late():
    """Late page"""
    query = conn.execute("SELECT * FROM [LDD.AppSheet_NO] WHERE Status LIKE '%LATE'")
    return render_template("/index.html", title="TnT - Late", query=query)


@app.route("/si", methods=["GET"])
def si():
    """SI page"""
    query = conn.execute("SELECT * FROM [LDD.AppSheet_NO] WHERE SICode IS NOT NULL")
    return render_template("/index.html", title="TnT - SI", query=query)


# need help with the search function
@app.route("/search")
def search():
    """Search page"""
    return render_template("/index.html", title="TnT - Search", query=query)


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
    tnt_url = rows[0][18]
    attachment1 = rows[0][19]
    attachment2 = rows[0][20]
    attachment3 = rows[0][21]
    attachment4 = rows[0][22]

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
    app.run(debug=True)

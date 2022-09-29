from flask import Flask, render_template, request, Response
from flask_cors import CORS
from sqlalchemy.orm import Session

from database_setup import engine
import models


models.Base.metadata.create_all(bind=engine)

session = Session(bind=engine)

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    """View for main page"""
    return render_template('index.html')


@app.route('/data/', methods=["post", "get"])
def data():
    """view for see inputs and get data from main"""
    if request.method == "POST":
        input = request.get_json()
        for index, data in enumerate(input):
            if data['value'] != "":
                data = {data['name']: data['value']}
                new_input = models.InputItem(data)
                session.add(new_input)
                session.commit()
        return Response(status=201)
    if request.method == "GET":
        data = session.query(models.InputItem).all()
        return render_template("input_list.html", data=data)

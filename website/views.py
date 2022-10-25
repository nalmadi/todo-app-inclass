
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Note
from flask_login import login_required, current_user

# for plotting things
import json
import plotly
import plotly.express as px

views = Blueprint('views', __name__)

# terrible idea, never do this:
# note = []

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    if request.method == "POST":
        note = request.form.get('item')
        new_note = Note(data=note, user_id=current_user.id)

        db.session.add(new_note)
        db.session.commit()

    #notes = list(db.session.query(Note).all())
    return render_template("home.html", user=current_user, active_page='home')


@views.route('/remove/<string:note_id>', methods=['GET'])
def remove(note_id):
    note = db.session.query(Note).filter_by(id=note_id).first()
    db.session.delete(note)
    db.session.commit()

    return redirect(url_for('views.home'))


@views.route('/figures', methods=['GET', 'POST'])
@login_required
def figures():

    df = px.data.medals_wide()
    fig = px.bar(df, x="nation", y=["gold", "silver", "bronze"], title="Medals", barmode="group")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("figures.html", user=current_user, graphJSON=graphJSON)
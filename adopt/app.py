from flask import Flask, render_template, flash, redirect, url_for, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet

from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.debug = True
# toolbar = DebugToolbarExtension(app)

app.app_context().push()
connect_db(app)
db.create_all()


@app.route("/")
def list_pets():
    """list pets"""

    pets = Pet.query.all()
    return render_template("pet_list.html", pets = pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """pet adding form; handle adding. """

    form = AddPetForm()

    if form.validate_on_submit():
        new_pet = Pet(name = form.name.data,
            species = form.species.data,
            photo_url = form.photo_url.data,
            age = form.age.data,
            notes = form.notes.data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"Added {new_pet.name}.")
        return redirect (url_for("list_pets"))
    
    else:
        return render_template("add_pet_form.html", form=form)

@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    """show details about pet and edit """


    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    
    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.photo_url = form.photo_url.data
        pet.available = form.available.data
        db.session.commit()
        flash(f'{pet.name} is updated')
        return redirect(url_for("list_pets"))
    
    else:
        return render_template('edit_pet_form.html', form=form, pet=pet)

@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):
    """Return basic info about pet in JSON."""

    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}

    return jsonify(info)
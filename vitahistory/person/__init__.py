from flask import Blueprint, redirect, render_template, request, url_for, flash, abort
from flask_login import current_user, login_required
from vitahistory.tools import get_current_time, save_picture
from vitahistory.models import Person, History, Category
from vitahistory import db


person = Blueprint('person', __name__, url_prefix='/person')


@person.route("/persons")
@login_required
def persons():
    page = request.args.get('page', 1, type=int)
    persons = Person.query.filter_by(user_id=current_user.id).order_by(Person.date_in.desc()).paginate(page=page, per_page=3)


    image_user = url_for('static', filename='image/' + current_user.image_user)


    return render_template('person/persons.html', persons=persons, image_user=image_user)



@person.route("/create", methods=["POST", "GET"])
@login_required
def create_person():
    if request.method == "POST":
        fullname = request.form["fullname"].title()
        email = request.form["email"]
        prefix_number = request.form["prefix_number"]
        sufix_number = request.form["sufix_number"]
        date_in = get_current_time()
        category = request.form["category"]

    
        phonenumber = prefix_number + sufix_number

        if len(phonenumber) > 11:

            flash('El número telefónico excede la cantidad de digitos')
            return redirect(url_for('person.create_person'))

        elif len(phonenumber) < 11:

            flash('El número telefónico no cumple la cantidad de digitos')
            return redirect(url_for('person.create_person'))

        image_person = None

        if request.files["picture"]:
            user_picture = request.files["picture"]
            picture_file = save_picture(user_picture)

            image_person = picture_file


        error1 = None
        error2 = None

        if email:
            person_email = Person.query.filter_by(email=email).first()
            if isinstance(person_email, Person):
                error1 = "Correo electrónico repetido"

        if phonenumber:
            person_number = Person.query.filter_by(phonenumber=phonenumber).first()
            if isinstance(person_number, Person):
                error2 = "Número telefónico repetido"

        if error1 is None and error2 is None:
            if image_person is not None:
                person = Person(fullname=fullname, email=email, phonenumber=phonenumber, \
                        date_in=date_in, image_person=image_person, user_id=current_user.id, category=category)

            else:
                person = Person(fullname=fullname, email=email, phonenumber=phonenumber, \
                        date_in=date_in, user_id=current_user.id, category=category)

            db.session.add(person)
            db.session.commit()

            return redirect(url_for('person.persons'))

        if error1 is not None:
            flash(error1)
        if error2 is not None:
            flash(error2)

    categories = Category.query.filter_by(user_id=current_user.id).all()

    page = request.args.get('page', 1, type=int)
    persons = Person.query.filter_by(user_id=current_user.id).order_by(Person.date_in.desc()).paginate(page=page, per_page=3)


    image_user = url_for('static', filename='image/' + current_user.image_user)

    return render_template('person/create_person.html', categories=categories, persons=persons, image_user=image_user)


@person.route("/show/categories", methods=["POST", "GET"])
@login_required
def show_categories():


    categories = Category.query.filter_by(user_id=current_user.id).all()

    persons = Person.query.filter_by(user_id=current_user.id).paginate()


    image_user = url_for('static', filename='image/' + current_user.image_user)


    return render_template('person/show_categories.html', categories=categories, persons=persons, image_user=image_user)


@person.route("/create/category", methods=["POST", "GET"])
@login_required
def create_category():
    if request.method == "POST":


        if request.form["formulario"] == "1":
            category = request.form["category"].capitalize()

            cat_instance = Category.query.filter_by(name=category).filter_by(user_id=current_user.id).first()

            error1 = None

            if isinstance(cat_instance, Category):
                error1 = 'La categoría ya está registrada en tu cuenta'


            if error1 is None:
                category = Category(name=category, user_id=current_user.id)
                db.session.add(category)
                db.session.commit()

                return redirect(url_for('person.show_categories'))

            if error1 is not None:
                flash(error1)

    categories = Category.query.filter_by(user_id=current_user.id).all()

    page = request.args.get('page', 1, type=int)
    persons = Person.query.filter_by(user_id=current_user.id).order_by(Person.date_in.desc()).paginate(page=page, per_page=3)


    image_user = url_for('static', filename='image/' + current_user.image_user)

    return render_template('person/create_category.html', categories=categories, persons=persons, image_user=image_user)


@person.route("/delete/category/<int:category_id>", methods=["POST", "GET"])
@login_required
def delete_category(category_id):

    category = Category.query.filter_by(id=category_id).first_or_404()

    if request.method == "POST":

        category = Category.query.filter_by(id=category_id).first_or_404()
        
        persons = Person.query.filter_by(user_id=current_user.id).filter_by(category=category.name).all()

        for person in persons:
            person.category = "Sin categoría"

        db.session.delete(category)
        db.session.commit()

        return redirect(url_for('person.show_categories'))



    categories = Category.query.filter_by(user_id=current_user.id).all()

    persons = Person.query.filter_by(user_id=current_user.id).paginate()

    image_user = url_for('static', filename='image/' + current_user.image_user)

    return render_template('person/delete_category.html', category=category, categories=categories, persons=persons, image_user=image_user)


@person.route("/edit_person/<int:person_id>", methods=["GET", "POST"])
@login_required
def edit_person(person_id):

    person = Person.query.filter_by(id=person_id).first_or_404()

    if person.author != current_user:
        abort(403)

    if request.method == "POST":
        fullname = request.form["fullname"].title()
        email = request.form["email"]
        phonenumber = request.form["phonenumber"]
        category = request.form["category"]

        if len(phonenumber) > 11:

            flash('El número telefónico excede la cantidad de digitos')
            return redirect(url_for('person.edit_person', person_id=person_id))

        elif len(phonenumber) < 11:

            flash('El número telefónico no cumple la cantidad de digitos')
            return redirect(url_for('person.edit_person', person_id=person_id))
    
        image_person = None

        if request.files["picture"]:
            user_picture = request.files["picture"]
            picture_file = save_picture(user_picture)

            image_person = picture_file


        error1 = None
        error2 = None

        if person.email != email:
            if email:
                person_email = Person.query.filter_by(email=email).first()
                if isinstance(person_email, Person):
                    error1 = "Correo electrónico repetido"

        if person.phonenumber != phonenumber:
            print(person.phonenumber, phonenumber)
            if phonenumber:
                person_number = Person.query.filter_by(phonenumber=phonenumber).first()
                if isinstance(person_number, Person):
                    error2 = "Número telefónico repetido"


        if error1 is None and error2 is None:
            if image_person is not None:
                person.fullname = fullname
                person.email = email
                person.phonenumber = phonenumber
                person.image_person = image_person
                person.category = category

            else:
                person.fullname = fullname
                person.email = email
                person.phonenumber = phonenumber
                person.category = category

            db.session.commit()

            return redirect(url_for('person.persons'))

        if error1 is not None:
            flash(error1)
        if error2 is not None:
            flash(error2)

    categories = Category.query.filter_by(user_id=current_user.id).all()

    page = request.args.get('page', 1, type=int)
    persons = Person.query.filter_by(user_id=current_user.id).order_by(Person.date_in.desc()).paginate(page=page, per_page=3)


    image_user = url_for('static', filename='image/' + current_user.image_user)

    return render_template('person/edit_person.html', person=person, categories=categories, persons=persons, image_user=image_user)



@person.route("/delete/<int:person_id>", methods=["GET", "POST"])
@login_required
def delete_person(person_id):

    person = Person.query.get_or_404(person_id)

    if person.author != current_user:
        abort(403)

    if request.method == "POST":

        if request.form["formulario"] == "1":

            histories = History.query.filter_by(patient=person).all()
            for history in histories:
                db.session.delete(history)
                db.session.commit()



            db.session.delete(person)
            db.session.commit()

            flash('Paciente borrado exitosamente', 'success')
            return redirect(url_for('person.persons'))

    page = request.args.get('page', 1, type=int)
    persons = Person.query.filter_by(user_id=current_user.id).order_by(Person.date_in.desc()).paginate(page=page, per_page=3)
    image_user = url_for('static', filename='image/' + current_user.image_user)

    return render_template('person/delete_person.html', person=person, person_id=person_id, persons=persons, image_user=image_user)

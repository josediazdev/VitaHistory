from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from vitahistory.tools import get_current_time
from vitahistory.models import History, Person
from vitahistory import db
from flask_login import login_required, current_user

history = Blueprint('history', __name__, url_prefix='/history')

@history.route("/histories/<int:person_id>")
@login_required
def show_histories(person_id):

    person = Person.query.get_or_404(person_id)

    if person.author != current_user:
        abort(403)

    persons = Person.query.filter_by(user_id=current_user.id).order_by(Person.date_in.desc()).paginate()

    image_user = url_for('static', filename='image/' + current_user.image_user)


    histories = History.query.filter_by(person_id=person_id).order_by(History.date_out.desc()).all()

    return render_template('history/show_histories.html', histories=histories, person=person, persons=persons, image_user=image_user)

@history.route("/create_history/<int:person_id>", methods=["GET", "POST"])
@login_required
def create_history(person_id):
    person = Person.query.get_or_404(person_id)

    if person.author != current_user:
        abort(403)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        date_out = get_current_time()



        history = History(title=title, content=content, date_out=date_out, person_id=person_id)

        db.session.add(history)
        db.session.commit()

        return redirect(url_for('history.show_histories', person_id=person_id))

    persons = Person.query.filter_by(user_id=current_user.id).order_by(Person.date_in.desc()).paginate()

    image_user = url_for('static', filename='image/' + current_user.image_user)


    return render_template('history/create_history.html', person_id=person_id, person=person, persons=persons, image_user=image_user)





@history.route("/edit_history/<int:history_id>", methods=["GET", "POST"])
@login_required
def edit_history(history_id):

    history = History.query.filter_by(id=history_id).first_or_404()


    if history.patient.author != current_user:
        abort(403)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
    
        history.title = title
        history.content = content

        db.session.commit()

        flash('Historia editada exitosamente', 'success')
        return redirect(url_for('history.show_histories', person_id=history.patient.id))

    person = Person.query.get_or_404(history.patient.id)

    persons = Person.query.filter_by(user_id=current_user.id).order_by(Person.date_in.desc()).paginate()

    image_user = url_for('static', filename='image/' + current_user.image_user)

    return render_template('history/edit_history.html', history=history, persons=persons, image_user=image_user, person=person)



@history.route("/delete/<int:history_id>", methods=["GET", "POST"])
@login_required
def delete_history(history_id):

    history = History.query.filter_by(id=history_id).first_or_404()

    if history.patient.author != current_user:
        abort(403)

    if request.method == "POST":

        db.session.delete(history)
        db.session.commit()


        flash('Historia borrada exitosamente', 'success')
        return redirect(url_for('history.show_histories', person_id=history.patient.id))

    person = Person.query.get_or_404(history.patient.id)

    persons = Person.query.filter_by(user_id=current_user.id).order_by(Person.date_in.desc()).paginate()

    image_user = url_for('static', filename='image/' + current_user.image_user)

    histories = History.query.filter_by(person_id=history.patient.id).order_by(History.date_out.desc()).all()

    flash('Seguro que quieres borrar esta historia?', 'warning')
    return render_template('history/delete_history.html', history=history, person=person, persons=persons, image_user=image_user, histories=histories)






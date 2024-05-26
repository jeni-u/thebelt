from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.sighting import Sighting
from flask_app.models.user import User

@app.route('/new/sighting')
def newSighting():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(data)
    return render_template('addsighting.html',user=user)


@app.route('/create/sighting', methods=['POST'])
def createSighting():
    if 'user_id' not in session:
        return redirect('/')

    if not Sighting.validate_sighting(request.form):
        return redirect("/new/sighting")

    data = {
        'location': request.form['location'],
        'what_happened': request.form['what_happened'],
        'date_of_sighting': request.form['date_of_sighting'],
        'nr_of_sas': request.form['nr_of_sas'],
        'user_id': session['user_id']
    }
    Sighting.createSighting(data)
    return redirect('/dashboard')


@app.route('/edit/sighting/<int:id>')
def editSighting(id):
    if 'user_id' not in session:
        return redirect('/')

    sighting = Sighting.get_sighting_by_id(id)
    if not sighting:
        return redirect('/')
    loggedUser = User.get_user_by_id({'id': session['user_id']})
    if sighting['user_id'] != loggedUser['id']:
        return redirect('/')

    return render_template('editsighting.html', sighting=sighting, loggedUser=loggedUser)


@app.route('/update/sighting/<int:id>', methods=['POST'])
def updateSighting(id):
    if 'user_id' not in session:
        return redirect('/')

    sighting = Sighting.get_sighting_by_id(id)
    if not sighting:
        return redirect('/')
    
    loggedUser = User.get_user_by_id({'id': session['user_id']})
    if not loggedUser:
        return redirect('/')

    if sighting['user_id'] != loggedUser['id']:
        return redirect('/')

    updateData = {
        'location': request.form['location'],
        'what_happened': request.form['what_happened'],
        'date_of_sighting': request.form['date_of_sighting'],
        'nr_of_sas': request.form['nr_of_sas'],
        'id': id
    }
    
    if not Sighting.validate_sighting(updateData):
        return redirect(request.referrer)

    Sighting.update_sighting(updateData)
    return redirect('/dashboard')

    

@app.route('/delete/sighting/<int:id>')
def delete_sighting(id):
    if 'user_id' not in session:
        return redirect('/')

    sighting = Sighting.get_sighting_by_id(id)
    if not sighting:
        return redirect('/')

    user_id = session['user_id']
    if sighting['user_id'] != user_id:
        return redirect('/')


    Sighting.remove_all_skeptics(id)
    

    data = {'sighting_id': id}
    Sighting.delete_sighting(data)

    return redirect(request.referrer)



@app.route('/view/sighting/<int:id>')
def view(id):
    if 'user_id' not in session:
        return redirect('/')

    sighting = Sighting.get_sighting_by_id(id)
    loggedUser = User.get_user_by_id({'id': session['user_id']})
    user_id = Sighting.get_user_id_by_sighting_id(id)
    user = User.get_user_by_id({'id': user_id})
    user_first_name = Sighting.get_user_first_name_by_id(user_id)
    skeptic_info = Sighting.get_skeptics_info(id) 
    
    return render_template("view.html", sighting=sighting, loggedUser=loggedUser, user=user, user_first_name=user_first_name, skeptic_info=skeptic_info)





@app.route('/skeptic/<int:id>')
def click(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'sighting_id': id,
        'user_id': session['user_id']
    }

    if not Sighting.is_skeptic(data):
        Sighting.skeptic(data)

    return redirect(request.referrer)

@app.route('/believer/<int:id>')
def believer(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'sighting_id': id,
        'user_id': session['user_id'] 
    }
    Sighting.remove_skeptic(data)
    return redirect(request.referrer)


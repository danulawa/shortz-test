from ast import Delete
from datetime import datetime

from flask_login import login_required
from core.models import ShortUrls, UserInfo
from core import app, db
from random import choice
import string
from flask import render_template, request, flash, redirect, url_for
import sqlite3 as sql


# =====================================================
# Link Management
# =====================================================



def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        url = request.form['url']
        short_id = request.form['custom_id']

        if short_id and ShortUrls.query.filter_by(short_id=short_id).first() is not None:
            flash('Please enter different custom id!')
            return redirect(url_for('index'))

        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))

        if not short_id:
            short_id = generate_short_id(8)

        new_link = ShortUrls(original_url=url, short_id=short_id, created_at=datetime.now())
        db.session.add(new_link)
        db.session.commit()
        short_url = request.host_url + short_id

        all_data = ShortUrls.query.all()

        return render_template('index.html', short_url=short_url,datas=all_data)


    all_data = ShortUrls.query.all()
    return render_template("index.html",datas=all_data)



@app.route('/<short_id>')
def redirect_url(short_id):
    link = ShortUrls.query.filter_by(short_id=short_id).first()
    if link:
        return redirect(link.original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):

    if request.method == 'POST':

        url = request.form['url']
        short_id = request.form['custom_id']

        UpdatedUrl = ShortUrls.query.filter_by(id=id).first()

        UpdatedUrl.id = id
        UpdatedUrl.original_url = url
        UpdatedUrl.short_id = short_id
        
        db.session.commit()
        short_url = request.host_url + short_id

        all_data = ShortUrls.query.all()

        return render_template('index.html', datas=all_data)
    
    row_data = ShortUrls.query.filter_by(id=id).first()
    return render_template('update.html',datas=row_data)


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):

    DeleteRow = ShortUrls.query.filter_by(id=id).first()

    db.session.delete(DeleteRow)       
    db.session.commit()

    all_data = ShortUrls.query.all()

    return render_template('index.html', datas=all_data)


# =====================================================
# User Management
# =====================================================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username and UserInfo.query.filter_by(username=username).first() is not None:
            if password and UserInfo.query.filter_by(password=password).first() is not None:
                
                return redirect(url_for('index'))

# @app.route('/all-user', methods=['GET', 'POST'])
# def all_user():

#     if request.method == 'POST':
#         username = request.form['username']
#         usermail = request.form['usermail']
#         password = request.form['password']

#         if username and ShortUrls.query.filter_by(username=username).first() is not None:
#             flash('Please enter different username!')
#             return redirect(url_for('index'))

#         if not username:
#             flash('A username is required!')
#             return redirect(url_for('index'))

#         if not usermail:
#             flash('An e-mail is required!')
#             return redirect(url_for('index'))

#         if not password:
#             flash('An password is required!')
#             return redirect(url_for('index'))


#         new_user = UserInfo(username=username, usermail=usermail, password=password)
#         db.session.add(new_user)
#         db.session.commit()

#         all_users = UserInfo.query.all()
#         return render_template('users.html', datas=all_users)

#     all_users = ShortUrls.query.all()
#     return render_template("users.html",datas=all_users)

# @app.route('/update-user/<id>', methods=['GET', 'POST'])
# def update_user(id):

#     if request.method == 'POST':

#         url = request.form['url']
#         short_id = request.form['custom_id']

#         UpdatedUrl = UserInfo.query.filter_by(id=id).first()

#         UpdatedUrl.id = id
#         UpdatedUrl.original_url = url
#         UpdatedUrl.short_id = short_id
        
#         db.session.commit()
#         short_url = request.host_url + short_id

#         all_data = UserInfo.query.all()

#         return render_template('index.html', datas=all_data)
    
#     row_data = UserInfo.query.filter_by(id=id).first()
#     return render_template('update.html',datas=row_data)


# @app.route('/delete-user/<id>', methods=['GET', 'POST'])
# def delete_user(id):

#     DeleteRow = UserInfo.query.filter_by(id=id).first()

#     db.session.delete(DeleteRow)       
#     db.session.commit()

#     all_users = UserInfo.query.all()

#     return render_template('index.html', datas=all_users)
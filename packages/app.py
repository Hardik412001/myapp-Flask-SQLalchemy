
from curses.ascii import US
import numbers
from re import U
from flask import Flask, flash, jsonify,request ,make_response,Response
import json

import sqlite3

from extensions import db
from requests import session
from model import User,Contact
app  =   Flask(__name__)

app.secret_key='password'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/hardik/Public/packages/exp.sqlite3'
db.init_app(app)

@app.route('/entry',methods=['POST'])
def index():
    data=request.get_json()
    print(data)
    name=data['name']
    location=data['location']
    new_entry=User(name=name,location=location)
    db.session.add(new_entry)
    db.session.commit()
    return make_response(jsonify({"id":new_entry.id}),200)



@app.route('/delete/<int:id>',methods=['delete'])
def delete(id):
    user_to_delete = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user_to_delete)
    db.session.commit()
    return make_response(jsonify({"id":user_to_delete.id}),200)

    

@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    return_value = User.get_user(id)
    return make_response(jsonify(return_value),200)



@app.route('/user',methods=['GET'])
def get_user():
    return make_response(jsonify({'Users': User.get_all_users()}))




@app.route('/user/<int:id>',methods=['PUT'])
def update_user(id):
    request_data = request.get_json()
    User.update_movie(id, request_data['name'], request_data['location']    )
    response = Response("Movie Updated", status=200, mimetype='application/json')
    return response



@app.route('/thread',methods=['GET'])
def thread():
    data=request.get_json()
    page_num=data['page_num']
    try_num=(data['entry_num']-1)
    threads=User.query.paginate(per_page=2, page=page_num, error_out=True)
    res={
        "total_pages":threads.pages,
        "res_per_page":threads.per_page,
        "total_res":threads.total,
        "location":threads.items[try_num].location,
        "name":threads.items[try_num].name,
        "current_page":threads.page
    }
    return make_response(jsonify(res))


@app.route('/entry/contact',methods=['POST'])
def con_index():
    data=request.get_json()
    print(data)
    user_id=data['user_id']
    p_num=data['p_num']
    new_entry=Contact(p_num=p_num,user_id=user_id)
    db.session.add(new_entry)
    db.session.commit()
    return make_response(jsonify({"id":new_entry.id}),200)




@app.route('/both',methods=['GET'])
def both():
    result=db.session.query(User,Contact).join(Contact).all()
    print(result)
    l = []
    for user, contact in result:
        d = [user.json(), contact.json()]
        l.append(d)
    print(l)
    return make_response(jsonify(l),200)




@app.route('/byname',methods=['GET'])
def by_name():
    data = request.get_json()
    name=data["name"]
    result=db.session.query(User,Contact).join(User).all()
    l=[]
    for user, contact in result:
        if user.name==name:
            d = [user.json(), contact.json()]
            l.append(d)

    return make_response(jsonify(l),200)

@app.route('/contacts',methods=['GET'])
def get_contact():
    return make_response(jsonify({'Contacts': Contact.get_all_contacts()}))

db.create_all()

if __name__== "__main__":
    
    app.run(debug=True)

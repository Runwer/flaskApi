#!flask/bin/python
from flask import request, render_template, make_response, session
import requests
import uuid
import json

def fp_cookie(html, otherid):
    if otherid != None:
        if 'user' in session:
            return render_template(html, userid = otherid)
        else:
            if request.cookies.get('user_id'):
                uid = request.cookies.get('user_id')
                session['user'] = uid
                return render_template(html, userid = otherid)
            else:
                uid = str(uuid.uuid1())
                resp = make_response(render_template(html, otherid))
                resp.set_cookie('user_id', uid, max_age=3110400000)
                session['user'] = uid
                return (resp)
    else:
        if 'user' in session:
            return render_template(html, userid = str(session['user']))
        else:
            if request.cookies.get('user_id'):
                uid = request.cookies.get('user_id')
                session['user'] = uid
                return render_template(html, userid = str(session['user']))
            else:
                uid = str(uuid.uuid1())
                resp = make_response(render_template(html))
                resp.set_cookie('user_id', uid, max_age=3110400000)
                session['user'] = uid
                return (resp)

def fp_cookie_top(html, otherid):

    if otherid != None:
        try:
            uri = "http://127.0.0.1:5000/moviedb/api/v1.0/toplist?username=" + str(otherid)
            uResponse = requests.get(uri)
        except requests.ConnectionError:
            return "Connection Error"
        Jresponse = uResponse.text
        data = json.loads(Jresponse)
        if 'user' in session:
            return render_template(html, userid = otherid, movlist = data)
        else:
            if request.cookies.get('user_id'):
                uid = request.cookies.get('user_id')
                session['user'] = uid
                return render_template(html, userid = otherid, movlist = data)
            else:
                uid = str(uuid.uuid1())
                resp = make_response(render_template(html, otherid, movlist = data))
                resp.set_cookie('user_id', uid, max_age=3110400000)
                session['user'] = uid
                return (resp)
    else:
        if 'user' in session:
            try:
                uri = "http://127.0.0.1:5000/moviedb/api/v1.0/toplist?username=" + str(session['user'])
                uResponse = requests.get(uri)
            except requests.ConnectionError:
                return "Connection Error"
            Jresponse = uResponse.text
            data = json.loads(Jresponse)
            return render_template(html, userid = str(session['user']), movlist = data)
        else:
            if request.cookies.get('user_id'):
                uid = request.cookies.get('user_id')
                session['user'] = uid
                try:
                    uri = "http://127.0.0.1:5000/moviedb/api/v1.0/toplist?username=" + str(session['user'])
                    uResponse = requests.get(uri)
                except requests.ConnectionError:
                    return "Connection Error"
                Jresponse = uResponse.text
                data = json.loads(Jresponse)
                return render_template(html, userid = str(session['user']), movlist = data)
            else:
                uid = str(uuid.uuid1())
                resp = make_response(render_template(html))
                resp.set_cookie('user_id', uid, max_age=3110400000)
                session['user'] = uid
                return (resp)




        
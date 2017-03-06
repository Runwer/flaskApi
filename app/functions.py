#!flask/bin/python
from flask import request, render_template, make_response, session
import uuid

def fp_cookie(html):
    if 'user' in session:
        return render_template(html)
    else:
        if request.cookies.get('user_id'):
            uid = request.cookies.get('user_id')
            session['user'] = uid
            return render_template(html)
        else:
            uid = str(uuid.uuid1())
            resp = make_response(render_template(html))
            resp.set_cookie('user_id', uid, max_age=3110400000)
            session['user'] = uid
            return (resp)
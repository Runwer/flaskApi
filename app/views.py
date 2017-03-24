#!flask/bin/python
from __future__ import print_function # In python 2.7
from app import app
from flask import Flask, jsonify, request, abort, session
from flask_cors import CORS, cross_origin
from Pagerank import pagerank
from functions import fp_cookie, fp_cookie_top
import operator
from dbDriver import findMovBattleRand, findMovBattleVs, findMov, insertEdge, findEdge, pctEdge, notSeen, getNotSeen, winPct
import uuid
import sys


#Needs to set this in a template used by all frontend views

#cors = CORS(app, resources={r"/*": {"origins": "*"}})
cors = CORS(app, resources={r"/*": {"origins": ["http://www.fliqpick.com", "http://flask-env.3cnseq7p2s.us-west-2.elasticbeanstalk.com", "http://127.0.0.1:5000"], "supports_credentials": True}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@app.route('/index.html')
def index():
    return fp_cookie('/index.html', None)


@app.route('/about.html')
def about():
    return fp_cookie('/about.html', None)


@app.route('/contact.html')
def contact():
    return fp_cookie('/contact.html', None)


@app.route('/toplist.html')
def toplisthtml():
    if request.args.get('userid') != None:
        otherid = request.args.get('userid')
    else:
        otherid = None
        print('No username from GET!', file=sys.stderr)
    return fp_cookie_top('/toplist.html', otherid)

#Get movies for Versus
@app.route('/moviedb/api/v1.0/movies', methods=['GET'])
@cross_origin()
def moviedb():
    moviecount = request.args.get('count', type=int)
    user_id = request.headers.get('X-USER-ID')
    if moviecount == 1:
        #Consider doing a double call, then see if id of first == id of vsmovie
        mov = getNotSeen(user_id)
        mov.append(request.args.get('vsmovie'))
        notSeen(user_id, request.args.get('dump'))
        return findMovBattleVs(mov)
    if moviecount == 2:
        return findMovBattleRand(getNotSeen(user_id))

@app.route('/moviedb/api/v1.0/edge', methods=['POST'])
@cross_origin()
def create_task():
    if not request.json or not 'win' in request.json:
        abort(400)
    newEdge = {"loose" : request.json['loose'], "win": request.json['win'], "uid": request.headers.get('X-USER-ID')}
    insertEdge(newEdge)
    return ("success"), 201

@app.route('/moviedb/api/v1.0/toplist', methods=['GET'])
@cross_origin()
def toplist():
    session_user = request.args.get('username')
    #wins = winPct(session_user)
    edges = findEdge(session_user)
    if len(edges) != 0:
        sortedtlist = pagerank(edges)[0]
        #sortedtlist = sorted(tlist.items(), key=operator.itemgetter(1), reverse=True)
        outmovs = []
        i = 1
        for movlis in sortedtlist:
            temp = findMov(movlis[0])
            if i == 1:
                toppoints = float(movlis[1])
            temp["points"] = ("%.0f" % (float(movlis[1])*100/toppoints))

            #temp["winpct"] = round(((float(wins[temp['id']]['wins'])/(wins[temp['id']]['wins']+wins[temp['id']]['los']))*100),1)
            outmovs.append(temp)
            if i == 20:
                break
            i += 1

        return jsonify(outmovs)
    else: return jsonify({})

@app.route('/moviedb/api/v1.0/moviepct', methods=['GET'])
@cross_origin()
def pctMovie():
    return jsonify(pctEdge(request.args.get('mov1'), request.args.get('mov2')))

@app.route('/moviedb/api/v1.0/winpct', methods=['GET'])
@cross_origin()
def winpcts():
    return jsonify(winPct(request.headers.get('X-USER-ID')))


@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also accessible
        by the client. """
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    resp.headers['Access-Control-Allow-Headers'] = request.headers.get(
        'Access-Control-Request-Headers', 'Authorization' )
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '10'
    return resp

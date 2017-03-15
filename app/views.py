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

cors = CORS(app, resources={r"/*": {"origins": "*"}})
#app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@app.route('/index.html')
def index():
    return fp_cookie('/index.html', None)

@app.route('/toplist.html')
def toplisthtml():
    if request.args.get('userid') != None:
        otherid = request.args.get('userid')
        print('Hello world!'+otherid, file=sys.stderr)
    else:
        otherid = None
        print('No username from GET!', file=sys.stderr)
    print(otherid, file=sys.stderr)
    return fp_cookie_top('/toplist.html', otherid)

#Get movies for Versus
@app.route('/moviedb/api/v1.0/movies', methods=['GET'])
@cross_origin()
def moviedb():
    moviecount = request.args.get('count', type=int)
    if moviecount == 1:
        #Consider doing a double call, then see if id of first == id of vsmovie
        mov = getNotSeen(session['user'])
        mov.append(request.args.get('vsmovie'))
        notSeen(session['user'], request.args.get('dump'))
        return findMovBattleVs(mov)
    if moviecount == 2:
        return findMovBattleRand(getNotSeen(session['user']))

@app.route('/moviedb/api/v1.0/edge', methods=['POST'])
@cross_origin()
def create_task():
    if not request.json or not 'win' in request.json:
        abort(400)
    newEdge = {"loose" : request.json['loose'], "win": request.json['win'], "uid": session['user']}
    insertEdge(newEdge)
    return ("success"), 201

@app.route('/moviedb/api/v1.0/toplist', methods=['GET'])
@cross_origin()
def toplist():
    session_user = request.args.get('username')
    wins = winPct(session_user)
    edges = findEdge(session_user)
    if len(edges) != 0:
        tlist = pagerank(edges)[0]
        sortedtlist = sorted(tlist.items(), key=operator.itemgetter(1), reverse=True)
        outmovs = []
        for movlis in sortedtlist:
            temp = findMov(movlis[0])
            temp["points"] = ("%.2f" % movlis[1])
            temp["winpct"] = round(((float(wins[temp['id']]['wins'])/(wins[temp['id']]['wins']+wins[temp['id']]['los']))*100),1)
            outmovs.append(temp)

        return jsonify(outmovs)
    else: return jsonify({})

@app.route('/moviedb/api/v1.0/moviepct', methods=['GET'])
@cross_origin()
def pctMovie():
    return jsonify(pctEdge(request.args.get('mov1'), request.args.get('mov2')))

@app.route('/moviedb/api/v1.0/winpct', methods=['GET'])
@cross_origin()
def winpcts():
    return jsonify(winPct(session['user']))
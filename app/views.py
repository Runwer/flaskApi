#!flask/bin/python
from app import app
from flask import Flask, jsonify, request, abort
import random
from flask_cors import CORS, cross_origin
from Pagerank import pagerank
import operator
from dbDriver import findMovBattleRand, findMovBattleVs, findMov, insertEdge, findEdge, pctEdge, notSeen, getNotSeen

uid = "5"


cors = CORS(app, resources={r"/*": {"origins": "*"}})
#app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


#Get movies for Versus
@app.route('/moviedb/api/v1.0/movies', methods=['GET'])
@cross_origin()
def moviedb():
    moviecount = int(request.args.get('count'))
    if moviecount == 1:
        #Consider doing a double call, then see if id of first == id of vsmovie
        mov = getNotSeen(uid)
        mov.append(request.args.get('vsmovie'))
        notSeen(uid, request.args.get('dump'))
        return findMovBattleVs(mov)
    if moviecount == 2:
        return findMovBattleRand(getNotSeen(uid))

@app.route('/moviedb/api/v1.0/edge', methods=['POST'])
@cross_origin()
def create_task():
    if not request.json or not 'win' in request.json:
        abort(400)
    newEdge = {"loose" : request.json['loose'], "win": request.json['win'], "user": request.json['user']}
    insertEdge(newEdge)
    return ("success"), 201

@app.route('/moviedb/api/v1.0/toplist', methods=['GET'])
@cross_origin()
def toplist():
    edges = findEdge(uid)
    if len(edges) != 0:
        tlist = pagerank(edges)[0]
        sortedtlist = sorted(tlist.items(), key=operator.itemgetter(1), reverse=True)
        outmovs = []
        for movlis in sortedtlist:
            temp = findMov(movlis[0])
            temp["points"] = ("%.2f" % movlis[1])

            outmovs.append(temp)

        return jsonify(outmovs)
    else: return jsonify({})

@app.route('/moviedb/api/v1.0/moviepct', methods=['GET'])
@cross_origin()
def pctMovie():
    return jsonify(pctEdge(request.args.get('mov1'), request.args.get('mov2')))

#!flask/bin/python
from app import app
from flask import Flask, jsonify, request, abort
import random
from flask_cors import CORS, cross_origin
from Pagerank import pagerank
import operator
from dbDriver import findMovBattleRand, findMovBattleVs, findMov

uid = "1"


cors = CORS(app, resources={r"/*": {"origins": "*"}})
#app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


ids = [0,1,2,3,4,5,6,7,8]
edges = []

@app.route('/moviedb/api/v1.0/movies', methods=['GET'])
@cross_origin()
def moviedb():
    moviecount = int(request.args.get('count'))
    if moviecount == 1:
        #Consider doing a double call, then see if id of first == id of vsmovie
        mov = request.args.get('vsmovie')
        return findMovBattleVs(mov)
    if moviecount == 2:
        return findMovBattleRand()

@app.route('/moviedb/api/v1.0/edge', methods=['POST'])
@cross_origin()
def create_task():
    if not request.json or not 'win' in request.json:
        abort(400)
    newEdge = [request.json['loose'], request.json['win']]
    edges.append(newEdge)
    return jsonify(edges), 201

@app.route('/moviedb/api/v1.0/toplist', methods=['GET'])
@cross_origin()
def toplist():
    if len(edges) != 0:
        tlist = pagerank(edges)[0]
        sortedtlist = sorted(tlist.items(), key=operator.itemgetter(1), reverse=True)
        outmovs = []
        for movlis in sortedtlist:
            temp = findMov(movlis[0])
            temp["points"] = ("%.2f" % movlis[1])

            outmovs.append(temp)

        return jsonify(outmovs)
    else: return jsonify({'list': []})

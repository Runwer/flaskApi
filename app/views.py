#!flask/bin/python
from app import app
from flask import Flask, jsonify, request, abort
import random
from flask_cors import CORS, cross_origin
from Pagerank import pagerank
import operator
from dbDriver import findmov


cors = CORS(app, resources={r"/*": {"origins": "*"}})
#app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


movies = [
    {"id": "0", "Title":"Interstellar", "Poster": "Interstellar", "Year":"2014" },
    {"id": "1", "Title":"Blade Runner", "Poster": "BladeRunner", "Year": "1982" },
    {"id": "2", "Title": "The Hobbit: the Battle of the Five Armies", "Poster": "TheHobbit_TheBattleoftheFiveArmies", "Year": "2014"},
     {"id": "3", "Title":"Metropolis", "Poster": "Metropolis", "Year": "1929" },
     {"id": "4", "Title":"Alien", "Poster": "Alien", "Year": "1979" },
    {"id": "5", "Title":"Gangs of Wasseypur", "Poster": "GangsofWasseypur", "Year": "2012", "Description": "A clash between Sultan and Shahid Khan leads to the expulsion of Khan from Wasseypur, and ignites a deadly blood feud spanning three generations." },
     {"id": "6", "Title":"Sin City", "Poster": "SinCity","Year":	"2005", "Description":	"A film that explores the dark and miserable town, Basin City, and tells the story of three different people, all caught up in violent corruption."},
    {"id": "7",	"Title":"Kind Hearts and Coronets","Poster": "KindHeartsandCoronets",	"Year":	"1949", "Description":	"A distant poor relative of the Duke of D'Ascoyne plots to inherit the title by murdering the eight other heirs who stand ahead of him in the line of succession."},
    {"id": "8",	"Title":"Song of the Sea", "Poster": "SongoftheSea",	"Year":	"2014", "Description":	"Ben, a young Irish boy, and his little sister Saoirse, a girl who can turn into a seal, go on an adventure to free the faeries and save the spirit world."}
]

ids = [0,1,2,3,4,5,6,7,8]
edges = []

@app.route('/moviedb/api/v1.0/movies', methods=['GET'])
@cross_origin()
def moviedb():
    moviecount = int(request.args.get('count'))
    if moviecount == 1:
        mov = int(request.args.get('vsmovie'))
        mov1 = random.choice(list(set(ids)-set([mov])))
        return jsonify({'movies': [movies[mov1]]})
    if moviecount == 2:
        return findmov()

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
        for mov in sortedtlist:
            outmovs.append({'id': mov[0], 'points': ("%.2f" % mov[1]), 'Title': movies[int(mov[0])]['Title'],
                            'Poster': movies[int(mov[0])]['Poster']
            })

        return jsonify({'list': outmovs})
    else: return jsonify({'list': []})

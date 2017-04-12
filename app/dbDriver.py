from pymongo import MongoClient
from jsonencoder import JSONEncoder
import json
import os
import collections
import operator


# uri = ('localhost')
# client = MongoClient(uri)
# db = client.moviesdb

current_folder = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_folder, 'mlab.json')) as data_file:
    mlab = json.load(data_file)

uri = "mongodb://{0}:{1}@ds143050-a0.mlab.com:43050,ds143050-a1.mlab.com:43050/fliqpick?replicaSet=rs-ds143050".format(mlab["username"], mlab["password"])

client = MongoClient(uri,
                    connectTimeoutMS=30000,
                    socketTimeoutMS=None,
                    socketKeepAlive=True)
db = client.get_default_database()

## functions that mess with moviesCol
def findMovBattleRand(notlist):
    query = [{"$match":
        {"id": {"$nin": notlist}} },
             {"$sample": {"size": 2}}]
    projection = [{"_id": 0, "Title": 1, "Poster": 1, "id":1}]  # 0 kommer ikke med, 1 kommer med
    movs = db.moviesCol.aggregate(query)
    return JSONEncoder().encode([m for m in movs])

def findMovBattleVs(vs):
    query = [{"$match":
        {"id": {"$nin": vs}} },
    {"$sample": {"size": 1}}]
    projection = [{"_id": 0, "Title": 1, "Poster": 1, "id":1}]  # 0 kommer ikke med, 1 kommer med
    movs = db.moviesCol.aggregate(query)
    return JSONEncoder().encode([m for m in movs])

def findMov(id):
    query = {"id":id}
    projection = {"_id": 0, "Title": 1, "Poster": 1, "id": 1, "Description": 1}
    return db.moviesCol.find_one(query, projection)

## functions that plays around with the Collection of edges
def insertEdge(edge):
    db.edges.insert(edge)

def findEdge(uid):
    query = {'uid':uid}
    edgesDict = db.edges.find(query)#.count()
    edges = []
    for e in edgesDict:
        edges.append([str(e["loose"]), str(e["win"])])
    return edges


def pctEdge(movid1, movid2):
    query = {"win":str(movid1), "loose": str(movid2)}
    w1 = db.edges.find(query).count()
    query = {"win":movid2, "loose": movid1}
    w2 = db.edges.find(query).count()
    if w1+w2 != 0:
        out1 = w1 * 100 / (w1 + w2)
        pctout = [out1, 100-out1]
        return pctout
    else:
        return [50,50]

def winPct(uid):
    query = {"uid": uid}
    projection = {"_id": 0, "movieID": 1}
    w1 = db.edges.find(query)
    movs = {}
    for i in w1:
        if i["win"] in movs:
            if 'wins' in movs[i["win"]]:
                movs[i["win"]]['wins'] += 1
            else:
                movs[i["win"]]['wins'] = 1
        else:
            movs[i["win"]] = {'wins': 1, 'los': 0}
        if i["loose"] in movs:
            if 'los' in movs[i["loose"]]:
                movs[i["loose"]]['los'] += 1
            else:
                movs[i["loose"]]['los'] = 1
        else:
            movs[i["loose"]] = {'los': 1, 'wins':0}
    return movs

### functions regarding the notSeen Collection
def notSeen(uid, movid):
    db.notSeenCol.insert({"uid": uid, "movieID": movid})

def getNotSeen(uid):
    query = {"uid": uid}
    projection = {"_id": 0, "movieID": 1}
    outq = db.notSeenCol.find(query, projection)
    outlist = list(set([q["movieID"] for q in outq]))
    return outlist

def findGlobalScore():
    movs = db.Globalranking.find().sort([("_id",-1)]).limit(1)
    ranklist = [m for m in movs]
    outdictrank = {}
    i = 1
    for m in ranklist[0]['ranking']:
        outdictrank[m[0]] = [m[1], i]
        i += 1
    return outdictrank

def notSeenList(uid):
    notseen = getNotSeen(uid)
    globalscore = findGlobalScore()
    recviews = {}
    for n in notseen:
        try:
            recviews[n] = globalscore[n]
        except:
            recviews[n] = [0, 'Not Rated']

    sorted_recviews = sorted(recviews.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_recviews




if __name__ == '__main__':
    print notSeenList("a6c2d736-0f59-11e7-bb6a-0a0407b0c80f")



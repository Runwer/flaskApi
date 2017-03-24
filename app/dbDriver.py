from pymongo import MongoClient
from jsonencoder import JSONEncoder

# uri = ('localhost')
# client = MongoClient(uri)
# db = client.moviesdb

uri = 'mongodb://veres:3cnseq7p2s@ds155509.mlab.com:55509/fliqpick'
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
    projection = {"_id": 0, "Title": 1, "Poster": 1, "id": 1}
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
    outlist = [q["movieID"] for q in outq]
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



if __name__ == '__main__':
    print winPct('2')


from pymongo import MongoClient
from jsonencoder import JSONEncoder

uri = ('localhost')

client = MongoClient(uri)

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
    query = {"user":uid}
    projection = {"_id": 0, "win": 1, "loose": 1}
    edgesDict = db.edges.find(query, projection)#.count()
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

### functions regarding the notSeen Collection
def notSeen(uid, movid):
    db.notSeenCol.insert({"uid": uid, "movieID": movid})

def getNotSeen(uid):
    query = {"uid": uid}
    projection = {"_id": 0, "movieID": 1}
    outq = db.notSeenCol.find(query, projection)
    outlist = [q["movieID"] for q in outq]
    return outlist



if __name__ == '__main__':
    for e in getNotSeen("5"):
        print e




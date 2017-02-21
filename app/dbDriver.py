from pymongo import MongoClient
from jsonencoder import JSONEncoder

#uri = 'mongodb://runwer:REM040160rem@ds155509.mlab.com:55509/fliqpick'
uri = ('localhost')


client = MongoClient(uri)#prod,
                     #connectTimeoutMS=30000,
                     #socketTimeoutMS=None,
                     #socketKeepAlive=True)

# producttion: db = client.get_default_database()
db = client.moviesdb


## functions that mess with moviesCol
def findMovBattleRand(notlist):
    query = [{"$match":
        {"id": {"$nin": notlist}} },
             {"$sample": {"size": 2}}]
    projection = [{"_id": 0, "Title": 1, "Poster": 1, "id":1}]  # 0 kommer ikke med, 1 kommer med
    movs = db.moviesCol.aggregate(query)
    out = []
    for m in movs:
        out.append(m)
    return JSONEncoder().encode(out)

def findMovBattleVs(vs):
    query = [{"$match":
        {"id": {"$nin": vs}} },
    {"$sample": {"size": 1}}]
    projection = [{"_id": 0, "Title": 1, "Poster": 1, "id":1}]  # 0 kommer ikke med, 1 kommer med
    movs = db.moviesCol.aggregate(query)
    out = []
    for m in movs:
        out.append(m)
    return JSONEncoder().encode(out)

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
    query = {"user": uid}
    projection = {"_id": 0, "movieID": 1}
    outq = db.notSeenCol.find(query, projection)
    outlist = []
    for q in outq:
        outlist.append(q["movieID"])
    return outlist



if __name__ == '__main__':
    for e in db.edges.find():
        print e




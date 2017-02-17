from pymongo import MongoClient
from jsonencoder import JSONEncoder

client = MongoClient('localhost', 27017)

db = client.moviesdb

def findMovBattleRand():
    query = [{"$sample": {"size": 2}}]
    projection = [{"_id": 0, "Title": 1, "Poster": 1, "id":1}]  # 0 kommer ikke med, 1 kommer med
    movs = db.moviesCol.aggregate(query)
    out = []
    for m in movs:
        out.append(m)
    return JSONEncoder().encode(out)

def findMovBattleVs(vs):
    query = [{"$match":
        {"id": {"$ne": vs}} },
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

#def findList(idlist):
#    query = [{"id":{"$in":idlist}}]
#    projection = [{"_id": 0, "Title": 1, "Poster": 1, "id": 1}]


def insertEdge(edge):
    db.edges.insert(edge)

def findEdge(uid, id):
    query = {"uid":uid, "head": id}
    projection = {"_id": 0, "uid":1}
    return db.edges.find(query, projection).count()




if __name__ == '__main__':
    print findEdge("1", "250")




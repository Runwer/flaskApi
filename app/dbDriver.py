from pymongo import MongoClient
from jsonencoder import JSONEncoder

client = MongoClient('localhost', 27017)

db = client.moviesdb

def findmov():
    query = [{"$sample": {"size": 2}}]
    projection = [{"_id": 0, "Title": 1, "Poster": 1, "id":1}]  # 0 kommer ikke med, 1 kommer med
    movs = db.moviesCol.aggregate(query)
    out = []
    for m in movs:
        out.append(m)
    return JSONEncoder().encode(out)

#def insertmovies():
#    for m in movies:
#        db.moviesCol.insert(m)

if __name__ == '__main__':
    print {'movies':findmov()}




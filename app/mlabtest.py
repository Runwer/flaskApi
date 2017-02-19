from pymongo import MongoClient

uri = 'mongodb://runwer:REM040160rem@ds155509.mlab.com:55509/fliqpick'

client = MongoClient(uri,
                     connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True)

db = client.get_default_database()
print db.collection_names()

moviesForInsert = [{ "Poster" : "Interstellar", "Year" : "2014", "id" : "32", "Title" : "Interstellar" },
{ "Poster" : "BladeRunner", "Year" : "1982", "id" : "138", "Title" : "Blade Runner" },
{ "Poster" : "TheHobbit_TheBattleoftheFiveArmies", "Year" : "2014", "id" : "251", "Title" : "The Hobbit: the Battle of the Five Armies" },
{ "Poster" : "Metropolis", "Year" : "1929", "id" : "111", "Title" : "Metropolis" },
{ "Poster" : "Alien", "Year" : "1979", "id" : "52", "Title" : "Alien" },
{ "Description" : "A clash between Sultan and Shahid Khan leads to the expulsion of Khan from Wasseypur, and ignites a deadly blood feud spanning three generations.", "Title" : "Gangs of Wasseypur", "Poster" : "GangsofWasseypur", "Year" : "2012", "id" : "250" },
{ "Description" : "A film that explores the dark and miserable town, Basin City, and tells the story of three different people, all caught up in violent corruption.", "Title" : "Sin City", "Poster" : "SinCity", "Year" : "2005", "id" : "247" },
{ "Description" : "A distant poor relative of the Duke of D'Ascoyne plots to inherit the title by murdering the eight other heirs who stand ahead of him in the line of succession.", "Title" : "Kind Hearts and Coronets", "Poster" : "KindHeartsandCoronets", "Year" : "1949", "id" : "248" },
{ "Description" : "Ben, a young Irish boy, and his little sister Saoirse, a girl who can turn into a seal, go on an adventure to free the faeries and save the spirit world.", "Title" : "Song of the Sea", "Poster" : "SongoftheSea", "Year" : "2014", "id" : "249" },
{"id":"1","Title":"The Shawshank Redemption", "Year":"1994", "Description" : "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", "Poster" : "TheShawshankRedemption"}]

for mfi in moviesForInsert:
    db.moviesCol.insert(mfi)

print db.collection_names()


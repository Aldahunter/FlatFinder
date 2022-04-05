from src.DBShield import DBShield

db = DBShield(R"C:\DATA\repos\FlatFinder\data\FlatFinder.db")
PlaceQuery = db.entries.PlaceQuery

pqs = db.query(PlaceQuery).all()
for pq in pqs:
    print(pq.id, pq.search_query, pq.place_id)
from db.database import cli

class AdsLogic:

    
    async def find_by_query(self, query):
        ads = cli.get_coll('ads')
        result = (await ads).find(query, {'_id': 0}).to_list(None)
        return await result
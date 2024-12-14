from BADUC import mongodb as cli

gmuteh = cli["GMUTE"]

from typing import List

class Gmute:
    @staticmethod
    async def gmute_list() -> List:
        """
        Fetch the list of globally muted users from the database.
        Replace this with the actual database call.
        """
        # Simulate database call; replace with actual query
        return [
            {"sender": 7009601543},
        ]

async def is_gmuted(sender_id):
    kk = await gmuteh.find_one({"sender_id": sender_id})
    return bool(kk)


async def gmute(sender_id, reason="#GMuted"):
    await gmuteh.insert_one({"sender_id": sender_id, "reason": reason})


async def ungmute(sender_id):
    await gmuteh.delete_one({"sender_id": sender_id})


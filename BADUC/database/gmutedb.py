from BADUC import mongodb as cli

gmuteh = cli["GMUTE"]


async def is_gmuted(sender_id):
    kk = await gmuteh.find_one({"sender_id": sender_id})
    return bool(kk)


async def gmute(sender_id, reason="#GMuted"):
    await gmuteh.insert_one({"sender_id": sender_id, "reason": reason})


async def ungmute(sender_id):
    await gmuteh.delete_one({"sender_id": sender_id})


# BADUC/database/gmutedb.py

from typing import List, Dict
from BADUC import mongodb as db

# Example: Assuming a "gmuted_users" collection/table in your database
async def gmute_list() -> List[Dict]:
    """
    Fetch the list of all globally muted users.

    Returns:
        List[Dict]: A list of dictionaries with user details.
    """
    query = "SELECT * FROM gmuted_users"  # Modify based on your database schema
    return await db.fetch_all(query)

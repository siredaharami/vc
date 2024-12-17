from datetime import datetime
from threading import RLock

from pytz import timezone  # Ensure you are using pytz for timezones
from config import TIME_ZONE as TZ  # TIME_ZONE should be a valid timezone string, e.g., "Asia/Kolkata"
from userbot.database import MongoDB  # Import the fixed MongoDB helper

INSERTION_LOCK = RLock()
ANTISPAM_BANNED = set()  # To cache gbanned users locally for quick lookups


class GBan(MongoDB):
    """Class for managing Global Bans (Gbans) in the userbot."""

    db_name = "gbans"

    def __init__(self) -> None:
        """Initialize the GBan class with the MongoDB collection."""
        super().__init__(self.db_name)

    def check_gban(self, user_id: int) -> bool:
        """Check if a user is globally banned."""
        with INSERTION_LOCK:
            return bool(self.find_one({"_id": user_id}))

    def add_gban(self, user_id: int, reason: str, by_user: int) -> str:
        """Add a user to the global ban list."""
        global ANTISPAM_BANNED
        with INSERTION_LOCK:
            # Check if the user is already gbanned
            if self.find_one({"_id": user_id}):
                self.update_gban_reason(user_id, reason)
                return "User already gbanned, reason updated."

            # Add new gban entry
            time_rn = datetime.now(timezone(TZ))
            self.insert_one(
                {
                    "_id": user_id,
                    "reason": reason,
                    "by": by_user,
                    "time": time_rn.strftime("%Y-%m-%d %H:%M:%S"),  # Human-readable time
                },
            )
            ANTISPAM_BANNED.add(user_id)
            return "User successfully gbanned!"

    def remove_gban(self, user_id: int) -> str:
        """Remove a user from the global ban list."""
        global ANTISPAM_BANNED
        with INSERTION_LOCK:
            if self.find_one({"_id": user_id}):
                self.delete_one({"_id": user_id})
                ANTISPAM_BANNED.discard(user_id)  # Remove from cache
                return "User successfully un-gbanned!"

            return "User is not gbanned!"

    def get_gban(self, user_id: int) -> tuple:
        """Get the reason and status of a user's global ban."""
        with INSERTION_LOCK:
            curr = self.find_one({"_id": user_id})
            if curr:
                return True, curr.get("reason", "No reason provided.")
        return False, ""

    def update_gban_reason(self, user_id: int, reason: str) -> str:
        """Update the reason for a user's global ban."""
        with INSERTION_LOCK:
            modified_count, _ = self.update({"_id": user_id}, {"reason": reason})
            return "Gban reason updated!" if modified_count else "Failed to update reason!"

    def count_gbans(self) -> int:
        """Count the total number of globally banned users."""
        with INSERTION_LOCK:
            return self.count()

    def list_gbans(self) -> list:
        """List all globally banned users."""
        with INSERTION_LOCK:
            return self.find_all()

    def load_from_db(self) -> None:
        """Load gbanned users into the local cache for quick access."""
        global ANTISPAM_BANNED
        with INSERTION_LOCK:
            gbanned_users = self.find_all()
            ANTISPAM_BANNED = {user["_id"] for user in gbanned_users}

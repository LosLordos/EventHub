import json
from repositories import EventRepository, UserRepository

class DataImporter:
    def __init__(self):
        self.event_repo = EventRepository()
        self.user_repo = UserRepository()

    def import_from_json(self, json_content):
        """
        Expects JSON structure:
        {
            "events": [ ... ],
            "users": [ ... ]
        }
        """
        data = json.loads(json_content)
        results = {"events": 0, "users": 0, "errors": []}

        # Import Users
        if "users" in data:
            for user_data in data["users"]:
                try:
                    # Check if exists
                    if not self.user_repo.get_by_email(user_data['email']):
                        self.user_repo.create(
                            email=user_data['email'],
                            password_hash=user_data.get('password_hash', 'default_hash'),
                            role=user_data.get('role', 'customer'),
                            display_name=user_data.get('display_name', 'Imported User')
                        )
                        results["users"] += 1
                except Exception as e:
                    results["errors"].append(f"User import failed: {str(e)}")

        # Import Events
        if "events" in data:
            for event_data in data["events"]:
                try:
                    self.event_repo.create(
                        venue_id=event_data['venue_id'],
                        title=event_data['title'],
                        description=event_data.get('description', ''),
                        start_time=event_data['start_time'],
                        base_price=event_data['base_price']
                    )
                    results["events"] += 1
                except Exception as e:
                    results["errors"].append(f"Event import failed: {str(e)}")
                    
        return results

class Contact:
    def __init__(self, api = None):
        self.id = 0
        self.name = ""
        self.first_name = ""
        self.last_name = ""
        self.responsible_user_id = 0
        self.group_id = 0
        self.created_by = 0
        self.updated_by = 0
        self.created_at = 0
        self.updated_at = 0
        self.is_deleted = False
        self.closest_task_at = 0
        self.custom_fields_values = {}
        self.account_id = 0
        self.tags = {}
        self.companies = {}
        self.leads = {}
        self.api = api
    def add_text_note(self, text:str):
        self.api.add_lead_text_note(lead=self, text=text)

    def from_json(self, json):
        self.id = json["id"]
        try:
            self.name = json["name"]
            self.first_name = json["first_name"]
            self.last_name = json["last_name"]
            self.responsible_user_id = json["responsible_user_id"]
            self.group_id = json["group_id"]
            self.created_by = json["created_by"]
            self.updated_by = json["updated_by"]
            self.created_at = json["created_at"]
            self.updated_at = json["updated_at"]
            self.is_deleted = json["is_deleted"]
            self.closest_task_at = json["closest_task_at"]
            self.custom_fields_values = json["_embedded"]["custom_fields_values"]
            self.account_id = json["account_id"]
            self.tags = json["_embedded"]["tags"]
            self.companies = json["_embedded"]["companies"]
        except:
            pass
        return self
# data/api_client.py
import requests

DJANGO_API_URL = "http://127.0.0.1:8000/api"

class APIClient:
    def __init__(self, base_url=DJANGO_API_URL):
        self.base_url = base_url

    def user_exists(self, chat_id):
        r = requests.get(f"{self.base_url}/users/exists/{chat_id}/")
        return r.json().get("exists", False)

    def get_is_user_administrator(self, chat_id):
        r = requests.get(f"{self.base_url}/users/is-admin/{chat_id}/")
        return r.json().get("administrator", False)

    def get_first_name(self, chat_id):
        r = requests.get(f"{self.base_url}/users/first-name/{chat_id}/")
        return r.json().get("first_name", None)

    def add_user(self, last_name, first_name, patronymic, us_group, username, chat_id):
        payload = {
            "last_name": last_name,
            "first_name": first_name,
            "patronymic": patronymic,
            "us_group": us_group,
            "username": username,
            "chat_id": chat_id,
        }
        r = requests.post(f"{self.base_url}/users/", json=payload)
        return r.status_code == 201

    def get_full_user_info(self, chat_id):
        r = requests.get(f"{self.base_url}/users/info/{chat_id}/")
        if r.status_code == 200:
            return r.json()
        return None

    def get_user_id(self, chat_id):
        r = requests.get(f"{self.base_url}/users/user-id/{chat_id}/")
        return r.json().get("user_id", None)

    def get_category_id_by_name(self, name):
        r = requests.get(f"{self.base_url}/categories/by-name/{name}/")
        return r.json().get("category_id", None)

    def get_all_categories(self):
        r = requests.get(f"{self.base_url}/categories/")
        return [c["name"] for c in r.json()]

    def get_subcategories_by_category(self, category_id):
        r = requests.get(f"{self.base_url}/subcategories/by-category/{category_id}/")
        return r.json()

    def get_subcategory_description(self, subcategory_id):
        r = requests.get(f"{self.base_url}/subcategories/{subcategory_id}/description/")
        return r.json()

    def add_dynamic_question(self, user_id, description, category_id):
        payload = {"user": user_id, "description": description, "category": category_id}
        r = requests.post(f"{self.base_url}/dynamic-questions/", json=payload)
        return r.status_code == 201

    def get_dynamic_question_by_category(self, category_name):
        r = requests.get(f"{self.base_url}/dynamic-questions/by-category-unanswered/{category_name}/")
        return r.json()

    def get_static_questions_by_category_name(self, category_name):
        r = requests.get(f"{self.base_url}/static-questions/by-category-name/{category_name}/")
        return r.json()

    def create_question(self, user_type, username, question):
        payload = {
            "user_type": user_type,
            "username": username,
            "question": question,
        }
        return requests.post(f"{self.base_url}/questions/create/", json=payload).status_code == 201

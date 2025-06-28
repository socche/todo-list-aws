import os
import unittest
import requests

BASE_URL = os.environ.get("BASE_URL")

class TestReadOnlyAPI(unittest.TestCase):
    
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "BASE_URL no está configurada")
        self.todo_id = "unidentificadorquenoexiste"

    def test_list_todos(self):
        print('Listando todos los TODOs...')
        url = BASE_URL + "/todos"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_todo_not_found(self):
        print('Probando GET con un ID no existente...')
        url = BASE_URL + f"/todos/{self.todo_id}"
        response = requests.get(url)
        self.assertIn(response.status_code, [404, 500])


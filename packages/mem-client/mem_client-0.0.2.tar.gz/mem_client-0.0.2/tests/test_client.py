import unittest
from unittest.mock import patch, mock_open
import json
from mem_client.client import Client

class TestClient(unittest.TestCase):
    @patch('mem_client.client.requests.post')
    def test_create_mem(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"id": "12345"}

        client = Client(api_access_token="fake_token")
        response = client.create_mem(content="Test mem")

        self.assertEqual(response, {"id": "12345"})
        mock_post.assert_called_once()

    @patch('mem_client.client.requests.post')
    def test_create_mem_from_file(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"id": "67890"}
        mock_open = mock_open(read_data="# Test Mem\n\nThis is a test mem.")

        with patch('mem_client.client.open', mock_open):
            client = Client(api_access_token="fake_token")
            response = client.create_mem_from_file(file_path="test.md")

        self.assertEqual(response, {"id": "67890"})
        mock_post.assert_called_once()

    @patch('mem_client.client.requests.post')
    def test_batch_create_mems(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"memIds": ["12345", "67890"]}

        client = Client(api_access_token="fake_token")
        batch_mems = [
            {"content": "Test mem 1"},
            {"content": "Test mem 2"}
        ]
        response = client.batch_create_mems(batch_mems)

        self.assertEqual(response, {"memIds": ["12345", "67890"]})
        mock_post.assert_called_once()

    @patch('mem_client.client.requests.post')
    def test_append_to_mem(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"id": "12345"}

        client = Client(api_access_token="fake_token")
        response = client.append_to_mem(mem_id="10000000-0000-4000-a000-000000000000", content="This is an appended content.")

        self.assertEqual(response, {"id": "12345"})
        mock_post.assert_called_once()

    @patch('mem_client.client.requests.post')
    def test_handle_error_responses(self, mock_post):
        client = Client(api_access_token="fake_token")

        # Test 400 Bad Request
        mock_post.return_value.status_code = 400
        with self.assertRaises(ValueError):
            client.create_mem(content="Test mem")

        # Test 401 Unauthorized
        mock_post.return_value.status_code = 401
        with self.assertRaises(PermissionError):
            client.create_mem(content="Test mem")

        # Test 404 Not Found
        mock_post.return_value.status_code = 404
        with self.assertRaises(FileNotFoundError):
            client.create_mem(content="Test mem")

        # Test 429 Rate Limited
        mock_post.return_value.status_code = 429
        with self.assertRaises(ConnectionError):
            client.create_mem(content="Test mem")

        # Test 500 Server Error
        mock_post.return_value.status_code = 500
        with self.assertRaises(RuntimeError):
            client.create_mem(content="Test mem")

if __name__ == '__main__':
    unittest.main()

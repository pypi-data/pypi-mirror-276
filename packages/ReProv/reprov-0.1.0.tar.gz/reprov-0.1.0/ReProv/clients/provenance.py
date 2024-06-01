import requests
from base_client import AbstractClient

class ProvenanceClient(AbstractClient):
    def __init__(self):
        super().__init__("provenance")

    def get_all(self):
        pass

    def get(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def capture(self, execution_id):
        url = f"{self.base_url}/capture/{execution_id}"
        return self._request("GET", url)

    def draw(self, execution_id):
        url = f"{self.base_url}/draw/{execution_id}"
        return self._download_file(url)


    def _handle_response(self, response):
        """
        Internal method to handle responses from requests.
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            self._handle_http_error(http_err)
            return None
        except Exception as err:
            print(f"An error occurred: {err}")
            return None

    def _download_file(self, url):
        """
        Internal method to handle file download.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.content
        except requests.exceptions.HTTPError as http_err:
            self._handle_http_error(http_err)
            return None
        except Exception as err:
            print(f"An error occurred: {err}")
            return None

    def update(self, execution_id):
            pass
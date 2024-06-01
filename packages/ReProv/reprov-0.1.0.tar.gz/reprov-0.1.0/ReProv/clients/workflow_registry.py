import requests
from base_client import AbstractClient
class WorkflowRegistryClient(AbstractClient):
    def __init__(self):
        super().__init__("workflow_registry")

    def get_all(self):
        """
        List all workflows.
        """
        url = f"{self.base_url}/"
        return self._request("GET", url)

    def get(self, registry_id):
        """
        Get details of a specific workflow by registry_id.
        """
        url = f"{self.base_url}/{registry_id}"
        return self._request("GET", url)

    def create(self, workflow_data, specification_file, input_file=None):
        """
        Register a new workflow.
        """
        url = f"{self.base_url}/register/"
        files = {
            'specification_file': open(specification_file, 'rb')
        }
        if input_file:
            files['input_file'] = open(input_file, 'rb')

        response = requests.post(url, headers=self.headers, files=files, data=workflow_data)
        return self._handle_response(response)

    def update(self, registry_id, workflow_data, specification_file, input_file=None):
        """
        Update an existing workflow by registry_id.
        """
        url = f"{self.base_url}/update/{registry_id}"
        files = {
            'specification_file': open(specification_file, 'rb')
        }
        if input_file:
            files['input_file'] = open(input_file, 'rb')

        response = requests.put(url, headers=self.headers, files=files, data=workflow_data)
        return self._handle_response(response)

    def delete(self, registry_id):
        """
        Delete a workflow by registry_id.
        """
        url = f"{self.base_url}/delete/{registry_id}"
        return self._request("DELETE", url)

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

import requests
from base_client import AbstractClient

class WorkflowExecutionClient(AbstractClient):
    def __init__(self):
        super().__init__("workflow_execution")

    def get_all(self):
        """
        List all executed workflows.
        """
        url = f"{self.base_url}/"
        return self._request("GET", url)

    def get(self, execution_id):
        """
        Get details of a specific workflow execution by execution_id.
        """
        url = f"{self.base_url}/{execution_id}"
        return self._request("GET", url)

    def create(self, registry_id):
        """
        Execute a workflow by registry_id.
        """
        url = f"{self.base_url}/execute/{registry_id}"
        files = {}
        if input_file:
            files['input_file'] = open(input_file, 'rb')

        response = requests.post(url, headers=self.headers, files=files, data=execution_data)
        return self._handle_response(response)

    def delete(self, execution_data):
        """
        Delete a specific workflow execution.
        """
        if isinstance(execution_data, int):
            url = f"{self.base_url}/delete/?registry_id={execution_data}"
        elif hasattr(execution_data, 'reana_name'):
            url = f"{self.base_url}/delete/?reana_name={execution_data.reana_name}"
        else:
            raise ValueError("execution_data must be an integer (registry_id) or an object with a reana_name attribute")
        
        return self._request("DELETE", url)
    
    def download_outputs(self, execution_id):
        """
        Download outputs of a specific workflow execution by execution_id.
        """
        url = f"{self.base_url}/outputs/{execution_id}"
        return self._download_file(url)

    def download_inputs(self, execution_id):
        """
        Download inputs of a specific workflow execution by execution_id.
        """
        url = f"{self.base_url}/inputs/{execution_id}"
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
from robot.api.deco import keyword, not_keyword
import os
import requests

class Storage:
    def __init__(self) -> None:
        self.user_id = os.getenv('USER_ID')
        self.service_key = os.getenv('SERVICE_KEY')
        self.base_url = os.getenv('BASE_URL')

    @keyword("Upload File", types={'file': 'str', 'file_name': 'str', 'folder_path': 'str'})
    def upload_file(self, file, file_name, folder_path):
        # read the file
        with open(file, 'rb') as f:
            file_data = f.read()
        
        # upload the file
        file_key = f"{folder_path}/{file_name}"
        url = f"{self.base_url}/file-storage/robot/upload?user_id={self.user_id}&&file_key={file_key}"
        headers = {'Service-Key': self.service_key}
        response = requests.post(url, data=file_data, headers=headers)
        response.raise_for_status()
        return response.json()

    @keyword("Download File", types={'file_path': 'str', 'file_name': 'str'})
    def download_file(self, file_path, file_name):
        url = f"{self.base_url}/file-storage/robot/presigned-url?user_id={self.user_id}&&file_path={file_path}"
        headers = {'Service-Key': self.service_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # save the file from the returned URL
        file_url = response.json()['url']
        response = requests.get(file_url)
        response.raise_for_status()
        with open(file_name, 'wb') as f:
            f.write(response.content)
        return file_name
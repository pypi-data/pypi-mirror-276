# functionality to deploy and run pipelines 
import mimetypes
import requests

import vectorshift
from vectorshift.pipeline import Pipeline
from vectorshift.consts import *

class Config:
    # For now, the config is just a wrapper for the API key
    def __init__(self, api_key = None, public_key = None, private_key = None):
        self.api_key = api_key or vectorshift.api_key
        self.public_key = public_key or vectorshift.public_key
        self.private_key = private_key or vectorshift.private_key

    # Save the pipeline as a new pipeline to the VS platform.
    def save_new_pipeline(self, pipeline: Pipeline) -> dict:
        # already implemented in the Pipeline class
        # save method will itself raise an exception if 200 isn't returned
        response = pipeline.save(
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
            update_existing=False
        )
        return response.json()

    # Update the pipeline, assuming it already exists in the VS platform.
    # Raises if the pipeline ID doesn't exist, or isn't in the VS platform.
    def update_pipeline(self, pipeline: Pipeline) -> dict:
        response = pipeline.save(
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
            update_existing=True
        )

        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()
    
    def fetch_files(self) -> list[dict]:
        response = requests.get(
            API_FILE_FETCH_ALL_ENDPOINT,
            headers={
                'Api-Key': self.api_key,
                'Public-Key': self.public_key,
                'Private-Key': self.private_key 
            }
        )
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    def upload_file(self, file:str, folder_id:str=None, filetype:str=None) -> dict:
        try:
            headers={
                'Api-Key': self.api_key,
                'Public-Key': self.public_key,
                'Private-Key': self.private_key 
            }
            # infer the file type
            if filetype is None:
                filetype = mimetypes.guess_type(file)[0]
            if filetype is None:
                raise ValueError(f'Could not determine file type of {file}. Please ensure the file name has an appropriate suffix.')

            with open(file, 'rb') as f:
                files = {'file': (file, f, filetype)}
                response = requests.post(
                    API_FILE_UPLOAD_ENDPOINT,
                    data={'folderId': folder_id},
                    headers=headers,
                    files=files,
                )
        except Exception as e:
            raise ValueError(f'Problem uploading file: {e}')
        print('Successfully uploaded file.')
        return response.json()

    def delete_files_by_id(self, file_ids:list[str]) -> dict:
        headers={
            'Api-Key': self.api_key,
            'Public-Key': self.public_key,
            'Private-Key': self.private_key 
        }
        response = requests.delete(
            API_FILE_DELETE_ENDPOINT,
            data={'file_ids': file_ids},
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(response.text)
        print('Successfully deleted file(s).')
        return response.json()
    
    def delete_files_by_name(self, file_names:list[str]) -> dict:
        headers={
            'Api-Key': self.api_key,
            'Public-Key': self.public_key,
            'Private-Key': self.private_key 
        }
        response = requests.delete(
            API_FILE_DELETE_BY_NAMES_ENDPOINT,
            data={'file_names': file_names},
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(response.text)
        print('Successfully deleted file(s).')
        return response.json()


VectorShift = Config
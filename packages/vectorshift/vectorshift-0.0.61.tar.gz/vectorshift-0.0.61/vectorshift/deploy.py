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
        return response

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

    def upload_file(self, file:str, folder_id:str = None) -> dict:
        try:
            headers={
                'Api-Key': self.api_key,
                'Public-Key': self.public_key,
                'Private-Key': self.private_key 
            }
            # infer the file type
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
        return response

VectorShift = Config
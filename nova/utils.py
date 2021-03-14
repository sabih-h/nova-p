import base64
import glob
import os
from pathlib import Path
from typing import Generator

import pandas as pd


from pprint import pprint
from io import StringIO

import boto3
from dotenv import load_dotenv, find_dotenv
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


BUCKET_NAME = os.environ.get('BUCKET_NAME')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

INITIAL_DATABASE = os.environ.get('INITIAL_DATABASE')
PORT = os.environ.get('PORT')
HOST = os.environ.get('HOST')

TABLENAME = 'final'



def get_outward_codes():
	"""
	Returns list of london outward codes
	"""
	utils_fp = Path(os.path.realpath(__file__))
	data_fp = utils_fp.parent.parent.joinpath('data/misc/london-outward-codes.csv')
	return pd.read_csv(data_fp)['outward_code'].str.lower().to_list()


def url_to_filename(url: str) -> str:
	return base64.b64encode(url.encode(encoding='utf-8')).decode(encoding='utf-8')


def filename_to_url(fp: str) -> str:
	return base64.b64decode(fp.encode(encoding='utf-8')).decode(encoding='utf-8')


def get_filepath(dir_path: str, filename: str) -> str:
	return os.path.join(dir_path, filename)


def get_files(dir_path: str) -> Generator[str, None, None]:
    """
    Returns a generator where each item is a filepath
    """
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            yield os.path.join(root, file)


def get_last_file(dir_path: str, prefix='', suffix='') -> str:
    """
    Returns the last file in directory by name
    """
    return max(glob.iglob(f'{dir_path}/{prefix}*{suffix}'), key=os.path.basename)


def get_url(base_url: str, search_type: str, location: str, page: int) -> str:
	request_data = {
		'search_type': search_type,
		'location_id': location,
		'page': page,
	}
	url = base_url.format(**request_data)
	return url


def process_df_columns(df, columns):
    """
    - Adds missing columns
    - removes extra columns
    - orders columns

    """
    df_columns = df.columns

    # add the missing columns with null values
    for column in columns:
        if column not in df_columns:
            df[column] = None

    # Select and Order columns
    df = df[columns]

    return df


def flatten_json(y):
    """
    Naively flattens a json.
    """
    out = {} 

    def flatten(x, name =''): 
        
        # If the Nested key-value 
        # pair is of dict type 
        if type(x) is dict: 
            
            for a in x: 
                flatten(x[a], name + a + '_') 
                
        # If the Nested key-value 
        # pair is of list type 
        elif type(x) is list: 
            
            i = 0
            
            for a in x:              
                flatten(a, name + str(i) + '_') 
                i += 1
        else:
            out[name[:-1]] = x 

    flatten(y) 
    return out


def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )


def get_filepaths(s3_client):
    contents = s3_client.list_objects_v2(Bucket=BUCKET_NAME).get('Contents', {})
    for content in contents:
        yield content.get('Key')



if __name__ == '__main__':

	print(get_outward_codes())

	pass



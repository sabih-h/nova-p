import base64
import os
from pathlib import Path

import pandas as pd


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


def get_filename(search_type: str, location: str, page: int) -> str:
	return '-'.join((search_type, location, str(page))) + '.json'


def get_filepath(dir_path: str, filename: str) -> str:
	return os.path.join(dir_path, filename)


def get_url(base_url: str, search_type: str, location: str, page: int) -> str:
	request_data = {
		'search_type': search_type,
		'location_id': location,
		'page': page,
	}
	url = base_url.format(**request_data)
	return url



if __name__ == '__main__':

	print(get_outward_codes())

	pass



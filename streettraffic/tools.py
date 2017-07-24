import pickle

def dump_data_object(obj: 'any serializable object', path: str) -> None:
	""" 
	input: obj: any_serializable_object(something like list, dataframe, dict, ...)

	This function serialize a data object and save it to path

	"""

	with open(path, 'wb') as handle:
		pickle.dump(obj, handle)


def load_data_object(path: str) -> 'cooresponding object':
	"""
	input: path: str(specify a path)

	This function open the file in specified path and return cooresponding data object

	"""

	with open(path, 'rb') as handle:
		data = pickle.load(handle)

	return data

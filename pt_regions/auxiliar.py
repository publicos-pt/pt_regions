import json
import os


def handler(obj):
    # see http://stackoverflow.com/a/2680060/931303
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def cache(file_name_format):
    """
    A decorator to cache the result of the function into a file. The result
    must be a dictionary. The result storage is in json.

    The decorator argument is the file name format. The format must contain the
    same number of positional arguments as the function

    E.g. 'd_{0}_{1}.json' for a function of 2 arguments.
    """
    def cache_function(function):
        def func_wrapper(*args, **kwargs):
            file_name = file_name_format.format(*args, **kwargs)
            try:
                with open(file_name, 'r', encoding='utf8') as cache_file:
                    data = json.load(cache_file)
            except IOError:
                data = function(*args, **kwargs)
                with open(file_name, 'w', encoding='utf8') as cache_file:
                    cache_file.write(json.dumps(data, ensure_ascii=False, indent=2,
                                                separators=(',', ': '),
                                                sort_keys=True, default=handler))

            return data
        return func_wrapper
    return cache_function


PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PATH, 'raw_data/')


NUMBER_OF_DISTRICTS = 29
NUMBER_OF_MUNICIPALITIES = 308
NUMBER_OF_COUNTIES = 3092

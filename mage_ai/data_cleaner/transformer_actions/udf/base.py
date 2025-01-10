import importlib
from typing import List, Dict


class BaseUDF:
    def __init__(self, df, arguments:List=None, code=None, options:Dict=None, kwargs:Dict=None):
        self.df = df
        self.arguments = arguments
        self.code = code
        self.options = options
        self.kwargs = kwargs

    def execute(self):
        pass


def execute_udf(udf_name, df, arguments, code, options, kwargs):
    udf_class = getattr(
        importlib.import_module(f'mage_ai.data_cleaner.transformer_actions.udf.{udf_name}'),
        udf_name.title().replace('_', ''),
    )
    return udf_class(df, arguments, code, options, kwargs).execute()

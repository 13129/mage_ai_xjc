from mage_ai.data_cleaner.column_types.constants import ColumnType
from mage_ai.data_cleaner.transformer_actions.udf.base import BaseUDF
import pandas as pd


class Addition(BaseUDF):
    def execute(self):
        col1 = self.arguments[0]
        df_result = self.df[col1]
        column_type = self.options.get("column_type", self.kwargs.get('column_types', {}).get(col1))

        if len(self.arguments) == 1 and 'value' not in self.options:
            raise Exception('Require second column or a value to add.')

        if len(self.arguments) > 1:
            for col in self.arguments[1:]:
                df_result = df_result + self.df[col]

        if self.options.get('value') is not None:
            df_result = self.__add_value(
                df_result,
                self.options['value'],
                column_type=column_type,
                options=self.options,
            )
        return df_result

    def __add_value(self, original_column, value, column_type=None, options=None):
        if options is None:
            options = {}
        if column_type == ColumnType.DATETIME:
            time_unit = options.get('time_unit', 'd')
            return (
                pd.to_datetime(original_column, utc=True) + pd.to_timedelta(value, unit=time_unit)
            ).dt.strftime('%Y-%m-%d %H:%M:%S')
        return original_column + value

import pandas as pd

class Formatter:
    """
    A class used to format data and header of a dataframe given in input
    """

    def format_header(self, df: pd.DataFrame):
        """
        Format the header in lower case without whitespace
        
        Args:
            df (pandas.DataFrame): The target dataframe for the format phase
        """
        columns = df.columns
        for column in columns:
            format_column = column.replace(" ", "_").lower()
            df = df.rename(columns={column: format_column})
        return df

import pandas as pd


class Formatter:
    """
    A class used to format data and header of a dataframe given in input
    """

    def format_header(self, df: pd.DataFrame, prefix : str = ""):
        """
        Format the header in lower case without whitespace
        
        Args:
            df (pandas.DataFrame): The target dataframe for the format phase
            prefix (str): It is an header prefix to add at each element of the header
        """
        columns = df.columns
        for column in columns:
            format_column = column.replace(" ", "_").lower()
            if(prefix != ""):
                if(not format_column.startswith(prefix, 0, len(prefix))):
                    format_column = prefix + '_' + format_column
            df = df.rename(columns={column: format_column})
        return df

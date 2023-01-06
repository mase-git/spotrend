import pandas as pd
import sys

class Checker:
    """
    Class for check the integrity of data into a pandas.DataFrame
    """
    
    def check_commons(self, df : pd.DataFrame, ref: str):
        """
        Check outliers in a common column into a pandas dataframe given in input

        Args:
            df (pandas.DataFrame): It is the current dataframe to analuze
            ref (str): It is the name of the attribute to check
        """
        try:
            lst = df[ref]
            item = None
            for i in range(len(lst)):
                el = lst[i]
                if item == None:
                    item = el
                else:
                    if el != item:
                        return False
            return True
        except KeyError:
            return False


    def check_index(self, element : str, lst : list, column : str):
        """
        Define the index of the element in the column into the list given in input

        Args:
            element (str): define the element to search in the collection
            lst (list): define the list of items to check index
            column (str): identify the column key into the dictionary into the items of the lst
        """
        for i in range(len(lst)):
            o = lst[i]
            if o[column] == element:
                return i
        return -1
                
    

    def check_unique(self, dataframe: pd.DataFrame, column : str ):
        """
        Check that a column is unique

        Args:
            dataframe (pandas.DataFrame): Dataframe of the current data to analyze
            column (str): name of the column to check the unique property
        """
        try:
            vals = list(dataframe[column])
            s = list(set(vals))
            if len(s) == len(vals):
                return True
            else:
                return False
        except ValueError:
            return False

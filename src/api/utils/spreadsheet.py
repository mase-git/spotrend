import pandas as pd
import re

class SpredsheetWriter():
    """
    SpreadsheetWriter is  class to manage data inside a spreadsheet. 
    It manages the raw Spotify data, organize sheet based on tags and generate the output file.
    """

    def generated_by_sheet_tags(self, dataframe: pd.DataFrame):
        """
        Generate a spreadsheet file with multiple sheets defined by a series of tags
        given by the headers of the columns inside the input dataframe.

        Args:
            dataframe (pandas.Dataframe): The data source for the output file
        """
        # define tags for sheet division
        tags = self.extract_tags(dataframe)

        # define attributes according to the tags division
        attributes = self.split_sheet_keys(dataframe, tags)

        # track sheet information, explicit way
        track_attributes = attributes['track']
        track_sheet = pd.DataFrame()

        # main sheet
        for attr in track_attributes:
            # insert data in the track sheet
            track_sheet[attr] = dataframe[attr]

        # insert sheets based on tags
        df = {}
        for tag in tags:
            df[tag] = pd.DataFrame()
            for attr in attributes[tag]:
                df[tag][attr] = dataframe[tag + ':' + attr]
                # available merging, so we need to refer to the track id
                df[tag]['track_id'] = track_sheet['id'] 

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('data/raw_spotify_data.xlsx', engine='auto')

        # Write each dataframe to a different worksheet.
        track_sheet.to_excel(writer, sheet_name='tracks')
        df['artists'].to_excel(writer, sheet_name='artists')
        df['album'].to_excel(writer, sheet_name='albums')
        df['feat'].to_excel(writer, sheet_name='features')

        writer.close()



    def split_sheet_keys(self, dataframe: pd.DataFrame, tags: list):
        """
        Defines the attributes name in the sheet division defined by the list of 
        tags given in input on the dataframe specified in the parameters of the function.

        Args:
            dataframe (pandas.Dataframe): The data source where to get the headers
            tags (list): List of tags (str) for the header classification
        """
        columns = list(dataframe.columns)

        # save in the attributes the list of headers organized by sheets
        sheet = {}

        # initialize sheets names
        for name in ['track', *tags]:
            sheet[name] = []

        # check for each column of the dataframe the tag matching
        for col in columns:
            insert = False
            for tag in tags:
                if len(col) >= len(tag) and col.startswith(tag, 0, len(tag)):
                    # trigger tag
                    name = col[len(tag)+1:]
                    try:
                        sheet[tag].append(name)
                    except ValueError:
                        sheet[tag] = [name]
                    insert = True
                    # we found it, so we need to break the check for less computation time
                    break
            if not insert:
                # it is one base attribute
                try:
                    sheet['track'].append(col)
                except ValueError:
                    sheet['track'] = [col]

        return sheet

    def extract_tags(self, dataframe: pd.DataFrame):
        """
        Given the input dataframe, defines the tags starting from the header format

        Args:
            dataframe (pandas.Dataframe): The data source for the output file
        """
        columns = list(dataframe.columns)
        pattern = re.compile(r'^\w+:\w+$')
        tags = set()
        for col in columns:
            if pattern.match(col):
                # extract the tag from the column name
                index = col.index(':')
                tag = col[:index]
                tags.add(tag)
        return list(tags)

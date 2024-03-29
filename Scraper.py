import pandas as pd
import openpyxl

"""
Scraper
Gather data from the parse_metadata tab of an excel file that contains values for the columns (datapoints) specified in column input file (currently meta_columns.txt)
Known bug - If you save an excel file using openpyxl (used to automate creation of the excel files), scrape_parse_tab function returns an empty dataframe.
"""

class Scraper():
    def __init__(self, columns, tab_name, **kwargs):
        self.achilles = 'Greatest genome-wide CRISPR screening team in the world'
        self.columns = columns #columns specified - currently meta_columns.txt
        self.tab_name = tab_name #name of the excel tab you wish to scrape

    #function to scrape an the 'parse_metadata' tab of an excel file
    def scrape_parse_tab(self, path, file_name):
        #attempt to find cell line sheet and load into pandas ExcelFile 
        excel_file = False
        try:
            excel_file = pd.ExcelFile(path + file_name, engine = 'openpyxl') #try to read the excel file using path and name from _get_filepaths.py
        except FileNotFoundError: #handle file not found
            print('Unable to find excel file with name: {} in {}'.format(file_name, path))
            raise Exception
        except Exception: #handle general exception
            print('Error loading excel file for {}'.format(file_name))
            raise Exception
        #if excel file was succesfully found, create a pandas df from only the parse_metadata tab
        if excel_file:
            try:
                tab_name = self.tab_name
                parse_tab_data = pd.read_excel(io = excel_file, sheet_name = tab_name) #read_excel to create sheet object
                parse_tab_data = parse_tab_data.set_index(self.columns[0]) #set index to first column listed in meta_columns.txt
                parse_tab_data['File Name'] = file_name #add file_name to dataframe for reference
                return parse_tab_data #return succesful parse
            except Exception: #handle general errors
                print('Unable to scrape {} from {}'.format(tab_name, file_name))
                raise Exception
            
    #scrape a list of excel files
    def scrape_list_of_lines(self, sheet_list_df):
        #create metadata dataframe to append new rows to
        metadata = pd.DataFrame(columns = self.columns)
        metadata = metadata.set_index(self.columns[0])
        
        #create empty lists to track succesful scrapes and failed scrapes
        success = []
        fails = []
        
        #for every file, attempt to scrape the data from the tab specified
        sheet_list_df = sheet_list_df.set_index('File Name')
        for index, row in sheet_list_df.iterrows():
            file_name = index
            path = row['Path']
            parse_tab_data = pd.DataFrame()    #if scraped succesfully, parse_tab_data will no longer be empty
            try:
                parse_tab_data = self.scrape_parse_tab(path, file_name) #see scrape_parse_tab above
            except Exception:
                fails.append(file_name)
                continue
            
            #append data to combined dataset (metadata)
            try:
                if not parse_tab_data.empty:    #if the scraped data is empty, do not try to append to metadata df
                    try:
                        #metadata = metadata.append(parse_tab_data, ignore_index = False, sort = False)
                        metadata = pd.concat([metadata, parse_tab_data], ignore_index = False, sort = False)
                        success.append(file_name)
                    except Exception:
                        print('Cannot append {} to metadata dataframe'.format(file_name))
                        fails.append(file_name)
                        continue
                else:
                    print('Parsed metadata empty for {}'.format(file_name))     #weird excel file bug where the data is on the xlsx file, but the read_excel function returns a blank row
                    fails.append(file_name)
                    
            except Exception:
                print('Error appending parsed data for {} to metadata dataframe'.format(file_name))
                fails.append(file_name)
                pass

        #return all scraped data as an output pandas df
        print('\n----------------------------------------------------------------')   #end error log 
        print('\n----------------------------------------------------------------\nScraped data from {} sheets\n----------------------------------------------------------------'.format(len(success))) #print the number of succesful scrapes/additions to metadata dataframe
        print('\n----------------------------------------------------------------\nMissing data from {} sheets: {}\n----------------------------------------------------------------'.format(len(fails), fails))  #print the number of failed scrapes and the names of the failed file_names

        return metadata

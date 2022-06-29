import re
from openpyxl import load_workbook
import pandas as pd

class Scraper():
    def __init__(self, columns, **kwargs):
        self.achilles = 'Greatest genome-wide CRISPR screening team in the world'
        self.columns = columns
        
    def scrape_parse_tab(self, path, file_name):
        #attempt to find cell line sheet and load into pandas ExcelFile 
        excel_file = False
        try:
            excel_file = load_workbook(''.join(path + file_name), data_only = True)
        except FileNotFoundError:
            print('Unable to find excel file with name: {} in {}'.format(file_name, path))
            raise Exception
        except Exception:
            print('Error loading excel file for {}'.format(file_name))
            raise Exception
        #if excel file was succesfully found, create a pandas df from only the parse_metadata tab
        if excel_file:
            """
            try:
                tab_name =  'parse_metadata'
                parse_tab = excel_file[tab_name]
                print(parse_tab)
                parse_tab_data = pd.DataFrame(columns = parse_tab.rows[0], values = parse_tab.rows[1])
                parse_tab_data['File Name'] = file_name
                return parse_tab_data
            except Exception:
                print('Unable to scrape {} from {}'.format(tab_name, file_name))
                raise Exception
            """
            
            tab_name =  'parse_metadata'
            parse_tab = excel_file[tab_name]
            
            columns = []
            for col in parse_tab[1]:
                columns.append(col.value)
            data = []
            for val in parse_tab[2]:
                data.append(val.value)
            
            parse_tab_data = pd.DataFrame(data = [data], columns = [columns])
            parse_tab_data['File Name'] = file_name
            return parse_tab_data
            
    #scrape a list of excel files
    def scrape_list_of_lines(self, sheet_list_df):
        #set columns to scrape from input to Scraper class instance
        metadata = pd.DataFrame(columns = self.columns)
        metadata = metadata.set_index('Achilles Screening Project ID')
        
        #create empty lists to track succesful scrapes and failed scrapes
        success = []
        fails = []
        
        #for every file, attempt to scrape the data from the parse tab
        sheet_list_df = sheet_list_df.set_index('File Name')
        for index, row in sheet_list_df.iterrows():
            file_name = index
            path = row['Path']
            parse_tab_data = pd.DataFrame()   #if scraped succesfully, parse_tab_data will no longer be empty
            parse_tab_data = self.scrape_parse_tab(path, file_name)
            
            """
            try:
                parse_tab_data = self.scrape_parse_tab(path, file_name)
            except Exception:
                fails.append(file_name)
                continue
            """
            #append data to combined dataset (termed metadata)
            try:
                if not parse_tab_data.empty:    #if the scraped data is empty, do not try to append to metadata df
                    try:
                        metadata = metadata.append(parse_tab_data.set_index('Achilles Screening Project ID'), ignore_index = False, sort = False)
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

        print(metadata)
        return metadata

"""
MAIN.PY -- Main script to run when scraping cell line sheets.
"""
def main():
    #create df of excel file names and paths in the common folders that have the parse metadata tab (based on name format 'NAME_LIBRARY_ASPID.xlsx')
    from _get_filepaths import get_filepaths
    file_paths = get_filepaths()

    #set tab name to be scraped
    tab_name = 'parse_metadata'

    #print number of sheets to scrape
    print('\n----------------------------------------------------------------\nAttempting to scrape {} tab from {} cell line sheets\n----------------------------------------------------------------\n'.format(tab_name, file_paths.shape[0]))    #inform user size of the inputted file
    
    #print divider for error log
    print('\n----------------------------------------------------------------\nError Log:\n')    #Errors will fall into this divider when printing into terminal

    #set columns of parse tab to scrape using column list from txt files in /columns_to_scrape
    with open(r'columns_to_scrape/meta_columns.txt', 'r') as column_file:
        columns = column_file.read()
        column_list = columns.split('\n')
        column_file.close()

    #create instance of Scraper class using column list as an input variable
    from Scraper import Scraper
    scraper = Scraper(column_list, tab_name)
    
    #scrape all sheets in the file_paths dataframe
    metadata = scraper.scrape_list_of_lines(file_paths)   #scrape data from each cell line listed in inputted file

    #save metadata as a csv file with the format 'parse_metadata_uniquedate'
    from datetime import datetime
    date = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = r'scraped_data/'     #store output file in this folder
    output_name = 'parsed_metadata_{}.csv'.format(date)      #include .csv in file name, and save date is appended
    from _save_metadata_df import save_metadata_df
    save_metadata_df(output_path, output_name, metadata)    #save dataframe using columns from meta_columns.txt

if __name__ == '__main__':
    main()

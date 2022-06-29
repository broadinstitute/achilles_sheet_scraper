INTRODUCTION

Hello Achilles Member!

This folder of python scripts and data was developed in order to ease the process of collecting the metadata from the screens performed. 

Achilles workflow requires each individual screen to have its own excel sheet, containing all of the assay data from that screen. 

The 'parse_metadata' tab was added to the excel sheets in October of 2021 for us to easily scrape metrics/data we consider valuable such as drug concentration, dates of assays, and much more. 

To run the script, simply run the main.py file within this folder using Python 3. See AUTOMATION below for instructions on setting up a cron job to automatically run this script without manual interevention.

REQUIRED MODULES 
See requirements.txt

FUNCTIONS
_get_filepaths.py: Contains the function get_filepaths(). This function goes through the folder containing all excel files and creates a pandas data frame of all sheets following the naming convention "STRIPPED CELL LINE NAME_ASP ID_LIBRARY.xlsx". All excel files named in this format contain the 'parse_metadata' tab. Screen excel files that do not follow that naming convention were created before the integration of the 'parse_metadata' tab. This data frame is saved to the "sheet_file_paths" folder and returned as an output when the function is called. This data frame of file names and paths is the default input to the scraper class i.e. the Scraper will get the metadata from every sheet within those folders.

_save_metadata_df.py: Contains the function save_metadata_df(output_path, output_name, metadata). This function saves the data frame containing all scraped metadata from a given run. The output is saved in the "scraped_data" folder. The data frame output will contain the columns specified in the "columns_to_scrape" folder.

Scraper.py: Contains the Class Scraper(self, columns, **kwargs). This class has the attribute: [columns] and contains the methods: [scrape_parse_tab(self, path, file_name), scrape_list_of_lines(self, sheet_list_df)]. The 'columns' attribute must be passed upon creation of an instance of the Scraper class. As a default, the columns to scrape and output columns are specified in the 'meta_columns.txt' file in the 'columns_to_scrape' folder. The 'scrape_parse_tab' function will return a df of the 'parse_metadata' tab for a given file name and path. The most common errors from this function will be when a given file is not found, the parse metadata tab does not exist or is named different in that file, or finally scraping an empty data frame from the file. The latter error can be fixed by creating a new parse_metadata tab on that excel file and pasting only the top two rows of the original 'parse_metadata' tab. Alternatively, it has been shown to be fixed by simply opening and saving the file as an excel workbook (.xlsx). The bug is caused by excel mistakenly denoting empty cells as cells containing data. The scrape_list_of_lines functions takes an input data frame containing the file_names and paths of all excel files to be scraped. By default this data frame is from the get_filepaths() function containing all excel files in the naming convention "STRIPPED CELL LINE NAME_ASP ID_LIBRARY.xlsx". 

main.py: 

APPLICATIONS REQUIRED
Python 3 - see requirements.txt for required modules
Google Drive

FILE LOCATIONS
All screen excel files are contained within the following path: /Volumes/GoogleDrive/Shared drives/GPP Cloud /Screening /Achilles/CRISPR/CRISPR screens

AUTOMATION
The main.py function can be automated to run at a given time using a cron job (for more information on cron jobs see here: https://www.hostinger.com/tutorials/cron-job). 

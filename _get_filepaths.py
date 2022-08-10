def get_filepaths():
    #function to create a list of cell line sheets in the format NAME_LIBRARY_ASPID.xlsx
    #return df with two columns: file name and general file path

    #create blank df 
    import pandas as pd
    meta_files_df = pd.DataFrame()

    #get all folders to search for files in from input file in /sheet_file_paths/input_folder_paths/folders_to_scrape.txt
    with open(r'folders_to_scrape/folders_to_scrape.txt') as folders:
        folder_paths = folders.read()
        folder_paths = folder_paths.split('\n')
        folders.close()

    for path in folder_paths:
        #get all files in a folder
        import os 
        files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]

        #create pandas df from file names and add column for folder path
        df = pd.DataFrame(files, columns = ['File Name'])
        df['Path'] = path

        #concatenate file dataframe for a given folder with rest of datframes
        meta_files_df = pd.concat([meta_files_df, df])
        
    #filter df to only cell line sheets in the correct naming format 
    name_format = True #Make False if you do not wish to have a naming convention
    
    if name_format:
        name_format = "^[a-zA-Z0-9]+_[a-zA-Z0-9]+_ASP[0-9]+.xlsx" #NAME_LIBRARY_ASPID.xlsx is current naming convention for lines that include parse_metadata
        filtered_sheet_df = meta_files_df[meta_files_df['File Name'].str.contains(name_format)] #filter df based on naming convention
    else:
        filtered_sheet_df = meta_files_df[meta_files_df['File Name'].str.contains('.xlsx')]

    #save file paths one file per month
    from datetime import datetime
    date = datetime.now().strftime("%Y%m")
    filtered_sheet_df.to_csv(r'folders_to_scrape/sheet_file_paths/file_paths_{}.csv'.format(date))

    return filtered_sheet_df

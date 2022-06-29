def get_filepaths():
    #function to create a list of cell line sheets in the format NAME_LIBRARY_ASPID.xlsx
    #return df with two columns: file name and general file path
    
    #declare variables for the two folder paths to search in (CRISPR Screens and Screens Completed Passaging)
    CRISPR_screens_path = r'/Volumes/GoogleDrive/Shared drives/GPP Cloud /Screening /Achilles/CRISPR/CRISPR screens/'
    Screens_completed_path = r'/Volumes/GoogleDrive/Shared drives/GPP Cloud /Screening /Achilles/CRISPR/CRISPR screens/Screens completed passaging/'

    #create list of all files in directory
    import os
    CRISPR_screens_files = [file for file in os.listdir(CRISPR_screens_path) if os.path.isfile(os.path.join(CRISPR_screens_path, file))]
    Screens_completed_files = [file for file in os.listdir(Screens_completed_path) if os.path.isfile(os.path.join(Screens_completed_path, file))]

    #create data frame for each file path
    import pandas as pd
    CRISPR_screens_df = pd.DataFrame(CRISPR_screens_files, columns = ['File Name'])
    CRISPR_screens_df['Path'] = CRISPR_screens_path
    Screens_completed_df = pd.DataFrame(Screens_completed_files, columns = ['File Name'])
    Screens_completed_df['Path'] = Screens_completed_path

    #converge both folder dfs to one df
    meta_sheet_df = pd.concat([CRISPR_screens_df, Screens_completed_df])

    #filter df to only cell line sheets in the correct naming format (NAME_LIBRARY_ASPID.xlsx)
    name_format = "^[a-zA-Z0-9]+_[a-zA-Z0-9]+_ASP[0-9]+.xlsx"
    filtered_sheet_df = meta_sheet_df[meta_sheet_df['File Name'].str.contains(name_format)]

    #uncomment this next line to scrape test excel files 
    #filtered_sheet_df = filtered_sheet_df[filtered_sheet_df['File Name'].str.contains('TEST')]
    #uncomment this next line to not include test sheets when scraping
    filtered_sheet_df = filtered_sheet_df[~filtered_sheet_df['File Name'].str.contains('TEST')]

    from datetime import datetime
    date = datetime.now().strftime("%Y%m")
    filtered_sheet_df.to_csv(r'sheet_file_paths/file_paths_{}.csv'.format(date))

    return filtered_sheet_df

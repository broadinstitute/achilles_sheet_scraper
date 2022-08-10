#clean up the dataframe
def clean_data(metadata, column_list):
    import pandas as pd
    metadata = metadata.reset_index()
    metadata = metadata.sort_values(by = column_list[0], ascending = True) #sort by column 1 in meta_columns.txt (currrently unique IDs)

    import numpy as np
    metadata = metadata.fillna(np.NAN)

    return metadata

#save generated metadata as a csv file
def save_metadata_df(output_path, output_name, metadata):
    #load meta_columns.txt to get columns to save
    #column order in meta_columns.txt will match order in output file
    column_file = open(r'columns_to_scrape/meta_columns.txt', 'r')
    columns = column_file.read()
    column_list = columns.split('\n')
    column_file.close()
    
    try:
        metadata = clean_data(metadata, column_list) #clean dataframe
        metadata.to_csv(output_path + output_name, columns = column_list) #save dataframe as csv file
        print('\n----------------------------------------------------------------\nSuccesfully saved metadata as {} in {}\n----------------------------------------------------------------\n'.format(output_name, output_path))
    except Exception:
        print('\n----------------------------------------------------------------\nError attempting to save {} in {}\n----------------------------------------------------------------\n'.format(output_name, output_path))
    

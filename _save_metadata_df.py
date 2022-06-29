#save generated metadata as a csv file
def save_metadata_df(output_path, output_name, metadata):
    column_file = open(r'columns_to_scrape/meta_columns.txt', 'r')
    columns = column_file.read()
    column_list = columns.split('\n')
    column_file.close()
    try:
        import pandas as pd
        metadata = metadata.reset_index()
        metadata.to_csv(output_path + output_name, columns = column_list)
        print('\n----------------------------------------------------------------\nSuccesfully saved metadata as {} in {}\n----------------------------------------------------------------\n'.format(output_name, output_path))
    except Exception:
        print('\n----------------------------------------------------------------\nError attempting to save {} in {}\n----------------------------------------------------------------\n'.format(output_name, output_path))
    

import pandas as pd
import os
import json

def load_config(config_file):
    """Load configuration from a JSON file."""
    with open(config_file, 'r') as f:
        return json.load(f)

def merge_multiple_dataframe(input_folder_path, output_folder_path, final_data_path, ingested_files_path):
    """Merge multiple dataframes and write to an output file."""
    df_list = []
    file_list = []

    for file_name in os.listdir(input_folder_path):
        file_path = os.path.join(input_folder_path, file_name)
        df = pd.read_csv(file_path)
        df_list.append(df)
        file_list.append(file_path + '\n')

    final_df = pd.concat(df_list, axis=0, ignore_index=True).drop_duplicates()

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    final_df.to_csv(final_data_path, index=False)
    
    with open(ingested_files_path, 'w') as f:
        f.writelines(file_list)

def main():
    config = load_config('config.json')

    input_folder_path = config['input_folder_path']
    output_folder_path = config['output_folder_path']
    final_data_name = config['final_data_name']
    ingested_files_name = config['ingested_files_name']

    final_data_path = os.path.join(output_folder_path, final_data_name)
    ingested_files_path = os.path.join(output_folder_path, ingested_files_name)

    merge_multiple_dataframe(input_folder_path, output_folder_path, final_data_path, ingested_files_path)

if __name__ == '__main__':
    main()

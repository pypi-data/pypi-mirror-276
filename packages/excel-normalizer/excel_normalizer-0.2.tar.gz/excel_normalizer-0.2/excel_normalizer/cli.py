# excel_normalizer/cli.py
import argparse
import pandas as pd
import mimetypes
import os

def get_file_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        return mime_type
    else:
        return 'Unknown file type'

def main():
    parser = argparse.ArgumentParser(description='Normalize all large numbers as text.')
    parser.add_argument('file', type=str, help='path to csv/xlsx')
    args = parser.parse_args()
    norm_name = args.file.split('.')
    norm_name.pop(-1)
    norm_name = '.'.join(norm_name) + '_NORMALIZED.xlsx'
    if not os.path.isfile(args.file):
        print('file does not exist')
        return
    file_type = get_file_type(args.file)
    try:
        if file_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            file = pd.read_excel(args.file, dtype='str')
        elif file_type == 'text/csv':
            file = pd.read_csv(args.file, dtype='str')
        elif file_type == 'text/plain':
            file = pd.read_csv(args.file, sep='\t', dtype='str')
        else:
            print(f'file type {file_type} is not supported')
            return

        file.to_excel(norm_name, index=False)
        print('success')
    except Exception as e:
        print('failed to parse file')
        return

if __name__ == '__main__':
    main()

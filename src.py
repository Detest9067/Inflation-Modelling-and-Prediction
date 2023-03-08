import pandas as pd
import chardet
import missingno as msno



def read_csv_file(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())  # detect encoding of file
    df = pd.read_csv(file_path, encoding=result['encoding'])
    return df
import os 
import pandas as pd
import config 
from drug_enum import DrugClass as DC

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
EXCEL_FILE_PATH = os.path.join(ROOT_PATH,'data/SDx_Stats_HW.xlsx')

def get_dataframe_from_sheet(sheetname):
    '''
    Get a dataframe from the given sheetname. If sheetname.csv file
    is found, then return the csv file, else read the Excel file and 
    create a csv file to improve read performance of the sheetname for 
    future analysis.

    :param sheetname: a sheetname that exists in the Excel file. (case-sensitive)
    :type sheetname: str
    '''
    if os.path.exists(os.path.join(ROOT_PATH, f'data/{sheetname}.csv')):
        
        return pd.read_csv(os.path.join(ROOT_PATH, f'data/{sheetname}.csv'), 
                            header=0)
    else:
        print(f'First time reading {sheetname} sheet. Please wait a few moment...')
        xl_df = pd.read_excel(EXCEL_FILE_PATH, 
                            sheet_name=sheetname,
                            header=0,
                            engine='openpyxl')

        xl_df.to_csv(os.path.join(ROOT_PATH, f'data/{sheetname}.csv'),
                    index=False)

        return xl_df

def df_to_csv(df, filename, index_required=False, return_filepath=True):

    # check if the `result` directory exists, if not, then create one
    if not os.path.exists(os.path.join(ROOT_PATH, 'result')):
        os.mkdir(os.path.join(ROOT_PATH, 'result'))

    output_path = os.path.join(ROOT_PATH, f'result/{filename}.csv')
    
    # write dataframe to CSV
    df.to_csv(output_path, index=index_required)

    if return_filepath:
        return output_path


def categorize_bacteria_class(specie):


    # Note: as there is a Gram Specie appear in
    # both Pos and Neg, so it will be categorized
    # as Other initially 
    if specie in config.GRAM_NEG_SPECIES and \
        specie in config.GRAM_POS_SPECIES:
        return 'Other'
    elif specie in config.GRAM_POS_SPECIES:
        return 'Positive'
    elif specie in config.GRAM_NEG_SPECIES:
        return 'Negative'
    else:
        return 'Other'

def is_specie_correctly_using_drug(row):

    current_drug = row['PlateMap']
    
    found_drug_panel = config.PLATE_MAPS.get(current_drug)
    if not found_drug_panel:
        return None

    if row['Species'] in config.GRAM_NEG_SPECIES:
        return found_drug_panel == DC.NEGATIVE.value
    
    elif row['Species'] in config.GRAM_POS_SPECIES:
        return found_drug_panel == DC.POSITIVE.value
    else:
        return None
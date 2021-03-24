import pandas as pd
import config 
import utils

def question1_1():
    '''
    1. How do you ensure data integrity in the metadata?
    
    STEP:
    1. Check data completeness
    2. Check data validation on categorical data
    '''
    metadata_df = utils.get_dataframe_from_sheet(config.METADATA_SHEETNAME)
    # 1. Check Data Integrity
    print('Check data completeness, data validation on categorical column if any unknown value found\n')
    print('- Sample data completeness check: Check number of empty value (NA) in each column')
    
    print('---result---')
    # null frequency of each column
    for col in metadata_df.columns:
        print(f'{col}: {metadata_df[col].isna().sum()}')

    print()
    print('- Sample data validation on categorical column : Check if PlatePosition column contain any value not listed in one of the following: LF, LR, RF, and RR')
   
    all_unique_plate_position = metadata_df['PlatePosition'].unique()
    found_plate_position_bool = pd.Series(all_unique_plate_position).isin(config.EXPECTED_PLATE_POSITION)
    found_plate_position = all_unique_plate_position[found_plate_position_bool]
    not_found_in_plate_position = all_unique_plate_position[~found_plate_position_bool]
    
    print('---result---')
    print(f'Plate Position : {len(found_plate_position)} matched found: {",".join(found_plate_position)}')
    print(f'Plate Position : {len(not_found_in_plate_position)} unmatched found: {",".join(not_found_in_plate_position)}\n')


def question1_2():
    '''
    2. Check any irregularities in the Species names 

    STEP:
    1. Get all Neg/Pos species listed in the Metadata dataset
    2. Filter species that are not in the given Gram Neg/Pos Species 

    Result:
    - What we found out is that there are 26 species not 
    listed in Gram Neg/Pos Species (var `not_neg_pos_species`)

    Also, the source table reference contains a duplicated Specie (E. faecalis)
    in both table, which is ambiguous.

    '''
    metadata_df = utils.get_dataframe_from_sheet(config.METADATA_SHEETNAME)
    # print(metadata_df['Species'].value_counts(dropna=False))

    all_species = metadata_df['Species'].unique()

    is_gram_neg_species = pd.Series(all_species).isin(config.GRAM_NEG_SPECIES)
    is_gram_pos_species = pd.Series(all_species).isin(config.GRAM_POS_SPECIES)

    # extract species from dataset
    # 2. Filter species that are not in the given Gram Neg/Pos Species 
    not_neg_pos_species = all_species[~is_gram_neg_species & ~is_gram_pos_species ] 

    # check species that exist in the Gram Neg/Pos Species 
    # either_neg_pos_species =  all_species[is_gram_neg_species | is_gram_pos_species ] 

    # check percentage of species 
    species_value_counts = metadata_df['Species'].value_counts(dropna=False)

    # species that are found in Gram Neg/Pos Species list
    # print(species_value_counts[either_neg_pos_species].sort_values(ascending=False))

    result1_2 = species_value_counts[not_neg_pos_species].sort_values(ascending=False)
    
    # export the result to CSV
    result_filepath = utils.df_to_csv(result1_2,'result1_2', True)
    
    print(f'There are {len(result1_2)} species not listed in Gram Neg/Pos Species ')
    print(f'\nFor result reference, go to "{result_filepath}"')
    print('\nNOTE: the source table reference contains a duplicated Specie (E. faecalis) in both table, which could make the result incorrect.\n')

def question1_3():
    '''
    3. Were any of the drug panels used with species of bacteria 
        belonging to a classification not designated for them?
        e.g. did any E. coli experiments run using a G-Pos plate 
        such as PM34 or SD-GPn?

    STEP:
    1. Flag if the specie in that record match the data we have. True if match, False if not.
    2. Filter only records where flag is False
    '''
    

    metadata_df = utils.get_dataframe_from_sheet(config.METADATA_SHEETNAME)
    
    is_drug_correctly_given = metadata_df.apply(utils.is_specie_correctly_using_drug, axis=1)

    # Species with wrongly given drug
    result1_3 = metadata_df[is_drug_correctly_given==False]['Species'].value_counts()
    
    # export the result to CSV
    result_filepath = utils.df_to_csv(result1_3, 'result1_3', True)
    
    print(f'There are {len(result1_3)} drug panels used with species of bacteria belonging to a classification not designated for them')
    print(f'\nFor result reference, go to "{result_filepath}"\n')

def question1_4():
    '''
    4. Add a classification column to the metadata table, 
        showing whether an experiment was for a Gram Positive or Gram Negative species.
        If the species is not listed above, use "Other" as the classification

    STEP:
    1. Create a UDF function that will categorize the specie class
    2. Pass the Species series to the UDF function and have the result
        assign to the new column
    '''

    metadata_df = utils.get_dataframe_from_sheet(config.METADATA_SHEETNAME)
    metadata_df['Bacteria_class'] = metadata_df['Species'].apply(utils.categorize_bacteria_class)
    # metadata_df['Bacteria_class'].value_counts()
    result_filepath = utils.df_to_csv(metadata_df, 'result1_4')

    print(f'The new column is added, called `Bacteria_class`')
    print(f'\nFor result reference, go to "{result_filepath}"\n')


def question1_5():
    '''
    5. Summarize the metadata, grouping by Bacterial Source, Classification, and Species, 
    and counting the number of experiments, number of unique strains.

    STEP:
    1. Make sure the data contain bacteria classification
    2. Group data and aggregate the result appropriately
    '''

    metadata_df = utils.get_dataframe_from_sheet(config.METADATA_SHEETNAME)

    metadata_df['Bacteria_class'] = metadata_df['Species'].apply(utils.categorize_bacteria_class)

    result1_5 = metadata_df.groupby(['Bacterial_Source','Bacteria_class', 'Species']).agg({'UniqueId':'count', 'Strain':'nunique'})

    result_filepath = utils.df_to_csv(result1_5,'result1_5', True)
    print(f'There are {len(result1_5)} grouped by Bacterial Source, Classification, and Species ')
    print(f'\nFor result reference, go to "{result_filepath}"\n')

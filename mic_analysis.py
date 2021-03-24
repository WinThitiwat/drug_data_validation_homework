import pandas as pd
import config 
import utils

def question2_1():
    '''
    2.1. Are there experiments in the metadata for which
    there are no results in the MIC sheet, and vice versa?
        If so, which uniqueids?

    STEP:
    1. Get UniqueIds from metadata that appear MIC 
    2. Find UniqueIds difference 

    result: `result2_1.csv` 
    '''
    metadata_df = utils.get_dataframe_from_sheet(config.METADATA_SHEETNAME)
    mic_df = utils.get_dataframe_from_sheet(config.MIC_SHEETNAME)

    # 1. Get UniqueIds from metadata that appear MIC 
    metadata_uid_in_mic = metadata_df['UniqueId'].isin(mic_df['UniqueId'])

    # len(metadata_df[~ metadata_uid_in_mic] )

    # 2. Find UniqueIds difference 
    result2_1 = metadata_df[~metadata_uid_in_mic]['UniqueId'].drop_duplicates()

    # export the result to CSV
    result_filepath = utils.df_to_csv(result2_1, 'result2_1')

    print(f'There are {len(result2_1)} UniqueIds from Metadata that are not in MIC sheet.')
    print(f'\nFor result reference, go to "{result_filepath}"\n')

def question2_2():
    '''
    2.2. Using only records that should be used for algorithm training, 
    and not excluded, which Species/Abx combination yields the highest accuracy (EA and CA)?

    Assumption: 
    - highest accuracy (EA and CA) means that EA and CA both equal 1

    STEP:
    1. Get records that is used for algorithm training and not excluded from the experiment
    2. Filter the above dataset by EA and CA = 1 (meaning that result is good)
    3. After getting algorithm training required and not excluded good result records
        get all combination pair of Species/Abs

    result: `result2_2.csv` 
    '''
    mic_df = utils.get_dataframe_from_sheet(config.MIC_SHEETNAME)

    # 1. Get records that is used for algorithm training and not excluded from the experiment
    is_used_for_algotrain = mic_df['LibraryBuild']==1 
    should_not_be_excluded = mic_df['Exclude']==0
    training_not_excluded = mic_df[is_used_for_algotrain & should_not_be_excluded] 

    # 2. Filter the above dataset by EA and CA = 1 (meaning that result is good)
    good_ca = mic_df['CA']==1
    good_ea = mic_df['EA']==1
    highest_accuracy = good_ca & good_ea
    highest_accuracy_result = training_not_excluded[highest_accuracy]

    # 3. After getting algorithm training required and not excluded good result records
    # get all unique pairs of Species/Abx from the highest accuracy
    result2_2 = highest_accuracy_result[['Species','Abx']].drop_duplicates()
    
    # export the result to CSV
    result_filepath = utils.df_to_csv(result2_2, 'result2_2')

    print(f'There are {len(result2_2)} Species/Abx combination yields the highest accuracy (EA and CA)')
    print(f'\nFor result reference, go to "{result_filepath}"\n')

def question2_3():
    '''
    2.3. Using only records that should be used for algorithm training, 
    and not excluded, which Species/Abx combination yields a result fastest?

    Assumption: fastest result means that the amount of time it took is less

    STEP:
    1. Get records that is used for algorithm training and not excluded from the experiment
    2. Filter the above dataset by TTR (mins)
    2.1 Remove records that have TTR (mins) = -1 
    2.2 Filter only records where TTR (mins) equals to its minimum value
    3. After getting algorithm training required and not excluded fastest result records
        get all combination pair of Species/Abs

    result: `result2_2.csv` 
    '''

    mic_df = utils.get_dataframe_from_sheet(config.MIC_SHEETNAME)
        
    # 1. Get records that is used for algorithm training and not excluded from the experiment
    is_used_for_algotrain = mic_df['LibraryBuild']==1 
    should_not_be_excluded = mic_df['Exclude']==0
    training_not_excluded = mic_df[is_used_for_algotrain & should_not_be_excluded] 

    # 2.1 Remove records that have TTR (mins) = -1
    training_not_excluded_ttr_gt_0 = training_not_excluded[training_not_excluded['TTR (mins)'] >= 0]
    # Get the fastest TTR (mins) value 
    fastest = training_not_excluded['TTR (mins)'] == training_not_excluded_ttr_gt_0['TTR (mins)'].min()

    # 2.2 Filter only records where TTR (mins) equals to its minimum value
    # extract only records that has TTR the least
    min_ttr_result = training_not_excluded[ fastest ]

    # 3. After getting algorithm training required and not excluded 
    # fastest evaluation records, get all combination pair of Species/Abs
    result2_3 = min_ttr_result[['Species','Abx']].drop_duplicates()

    # export the result to CSV
    result_filepath = utils.df_to_csv(result2_3, 'result2_3')

    print(f'There are {len(result2_3)} Species/Abx combination yields a result fastest')
    print(f'\nFor result reference, go to "{result_filepath}"\n')

def question2_4():
    '''
    2.4. Is the above accuracy skewed to one ArrayType vs. another?

    '''
    mic_df = utils.get_dataframe_from_sheet(config.MIC_SHEETNAME)

    # 1. Get records that is used for algorithm training and not excluded from the experiment
    is_used_for_algotrain = mic_df['LibraryBuild']==1 
    should_not_be_excluded = mic_df['Exclude']==0
    training_not_excluded = mic_df[is_used_for_algotrain & should_not_be_excluded] 

    # 2. Filter the above dataset by EA and CA = 1 (meaning that result is good)
    good_ca = mic_df['CA']==1
    good_ea = mic_df['EA']==1
    highest_accuracy = good_ca & good_ea
    highest_accuracy_result = training_not_excluded[highest_accuracy]
    
    # Check frequency of ArrayType if it's skewed to one of the ArrayType
    result2_4 = highest_accuracy_result['ArrayType'].value_counts(dropna=True)

     # export the result to CSV
    result_filepath = utils.df_to_csv(result2_4, 'result2_4', True)

    print(f'Regarding the skewness of accuracy dataset, go to "{result_filepath}"\n')

def question2_5():
    '''
    2.5. Summarize the MIC data, filling in the SpeciesAbx sheet, with each Species + Abx on its own line

    STEP:
    1. Get all combination of Species/Abx
    2. Extract all relevant data from each combination
    '''
    mic_df = utils.get_dataframe_from_sheet(config.MIC_SHEETNAME)

    # 1. Get all combination of Species/Abx
    species_abx_combination = mic_df[['Species','Abx']].drop_duplicates()

    # prepare empty dataframe for keeping result and export to a new CSV file
    species_abx_sheet_columns = [
        'Species',
        'Abx',
        'Total Experiments',
        '#S',
        '#R',
        '#uS',
        '#uR',
        '#uT',
        '# Errors',
        'Avg EA',
        'Avg CA',
        'Avg TTR',
        'Avg % Errors',
        'Norm Avg EA',
        'Norm Avg CA',
        'Norm % Errors'
    ]
    result2_5 = pd.DataFrame(columns = species_abx_sheet_columns)
    
    print('Processing to extract all relevant data from each combination. \nWait for a moment...')
    
    # 2. Extract all relevant data from each combination
    for _, row in species_abx_combination.iterrows():

        # extract relevant info 
        is_current_species = mic_df['Species']==row['Species']
        is_current_abx = mic_df['Abx']==row['Abx']
        current_species_abx_df = mic_df[is_current_species & is_current_abx]
        isin_susceptible = current_species_abx_df['Category'].isin(config.SUSCEPTIBLE)
        isin_resistant = current_species_abx_df['Category'].isin(config.RESISTANT)
        isin_intermediate = current_species_abx_df['Category'].isin(config.INTERMEDIATE)
        intermediate_unique_strain_cnt = current_species_abx_df[isin_intermediate]['Strain'].nunique()
        is_error_in_drug = current_species_abx_df['Error']==1
        
        # e.g. E. coli
        rSpecies = row['Species']

        # e.g. Meropenem
        rAbx = row['Abx']

        # Total number of uniqueids for the species/abx combo
        rTotal_experiment = current_species_abx_df['UniqueId'].count()
        
        # number of susceptible strains
        rSuscept_strain_cnt = current_species_abx_df[isin_susceptible]['Strain'].count()

        # number of resistant strains
        rResist_strain_cnt = current_species_abx_df[isin_resistant]['Strain'].count()

        # number of UNIQUE susceptible strains
        rSuscept_unique_strain_cnt = current_species_abx_df[isin_susceptible]['Strain'].nunique()
        
        # number of UNIQUE resistant strains
        rResist_unique_strain_cnt = current_species_abx_df[isin_resistant]['Strain'].nunique()

        # number of total unique strains (uS + uR + uI)
        rTotal_unique_strain_cnt = rSuscept_unique_strain_cnt + rResist_unique_strain_cnt + intermediate_unique_strain_cnt

        # number of errors for the combo
        rError_cnt = current_species_abx_df[is_error_in_drug]['UniqueId'].count()

        # average EA for the species/abx combo
        rAvg_ea = current_species_abx_df['EA'].mean()
        
        # average CA for the species/abx combo
        rAvg_ca = current_species_abx_df['CA'].mean()
        
        # average time to result for the species/abx combo
        rAvg_ttr = current_species_abx_df['TTR (mins)'].mean()

        # % of samples for this combo which had errors
        rAvg_error = rError_cnt / rTotal_experiment

        # average EA for the combo, normalized for the strain.  E.g. (EA for Strain 1 + EA for Strain 2 + EA for Strain 3)/3 unique strains
        rNorm_avg_ea = 'N/A'

        # average CA for the combo, normalized for the strain.  E.g. (CA for Strain 1 + CA for Strain 2 + CA for Strain 3)/3 unique strains
        rNorm_avg_ca = 'N/A'
        
        # % error for the combo, normalized for the strain.  E.g. (% error for Strain 1 + % error for Strain 2 + % error for Strain 3)/3 unique strains
        rNorm_avg_error = 'N/A'

        current_result = {
            'Species': rSpecies,
            'Abx': rAbx,
            'Total Experiments': rTotal_experiment,
            '#S': rSuscept_strain_cnt,
            '#R': rResist_strain_cnt,
            '#uS': rSuscept_unique_strain_cnt,
            '#uR': rResist_unique_strain_cnt,
            '#uT': rTotal_unique_strain_cnt,
            '# Errors': rError_cnt,
            'Avg EA': rAvg_ea,
            'Avg CA': rAvg_ca,
            'Avg TTR': rAvg_ttr,
            'Avg % Errors': rAvg_error,
            'Norm Avg EA': rNorm_avg_ea,
            'Norm Avg CA': rNorm_avg_ca,
            'Norm % Errors': rNorm_avg_error,
        }

        # append the result the the dataframe
        result2_5 = result2_5.append(current_result, ignore_index=True)
    
    # export the result to CSV  
    result_filepath = utils.df_to_csv(result2_5, 'result2_5')

    print(f'There are {len(result2_5)} Species/Abx unique combination')
    print(f'\nFor result reference, go to "{result_filepath}"\n')


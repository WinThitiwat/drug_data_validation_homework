'''
Note that this file is created to be used as source of truth.
In production, we are not expecting to have all source of truth data
in one file, but put in different file as granular as possible

'''
METADATA_SHEETNAME = 'Metadata'
MIC_SHEETNAME = 'MIC'

EXPECTED_PLATE_POSITION = {'LF', 'LR', 'RF', 'RR'}

GRAM_NEG_SPECIES = {
    'A. baumannii',
    'C. freundii',
    'C. koseri',
    'E. cloacae',
    'E. coli',
    'E. faecalis',
    'K. aerogenes',
    'K. oxytoca',
    'K. pneumoniae',
    'P. aeruginosa',
    'P. mirabilis'
}

GRAM_POS_SPECIES = {
    'E. faecalis',
    'E. faecium',
    'S. aureus',
    'S. epidermidis',
    'S. hominis',
    'S. lugdunensis',
}


    
PLATE_MAPS = {
    'blank': 'read meta',
    'cannot found': 'read meta',
    'MICSTREPP2': 'read meta',
    'MS_ESBL': 'read meta',
    'NM37': 'G-Neg',
    'NM43': 'G-Neg',
    'NM56': 'G-Neg',
    'PM34': 'G-Pos',
    'SD-GN1': 'G-Neg',
    'SD-GN2': 'G-Neg',
    'SD-GN3': 'G-Neg',
    'SD-GP1': 'G-Pos',
    'SD-GP2': 'G-Pos',
    'Toku_e': 'read meta'
}

ANTIBIOTICS = [
    'Amikacin',
    'Amoxicillin_Clavulanate',
    'Ampicillin',
    'Ampicillin_Sulbactam',
    'Aztreonam',
    'Cefazolin',
    'Cefepime',
    'Cefotaxime',
    'Cefotaxime_Clavulanate',
    'Cefoxitin',
    'Ceftazidime',
    'Ceftazidime_Clavulanate',
    'Ceftriaxone',
    'Cefuroxime',
    'Cephalothin',
    'Ciprofloxacin',
    'Ertapenem',
    'Gentamicin',
    'Imipenem ',
    'Levofloxacin',
    'Meropenem',
    'Moxifloxacin',
    'Nitrofurantoin',
    'Piperacillin',
    'Piperacillin_Tazobactam',
    'Tetracycline',
    'Tigecycline',
    'Tobramycin',
    'Trimethoprim_Sulfamethoxazole'
]

SUSCEPTIBLE = {
    'S',
    'Neg',
    'NR',
    'S*',
    'S**'
}

RESISTANT = {
    'R*',
    'R',
    'R**',
    'Pos',
    'Pos*',
}

INTERMEDIATE = {
    'I'
}

# A list of relevant columns from MIC sheet that
# is to be used for data manipulation. By specifying 
# the columns name explicitly, it helps remove the issue
# of referencing column if the columns order in a dataset 
# is changed.
mic_columns_of_focus = [
    'UniqueId',
    'Species',
    'Strain',
    'Abx',
    'TTR (mins)',
    'EA',
    'Category',
    'CA',
    'Error',
    # 'Instrument',
    # 'Bacterial_Source',
    'ArrayType',
    'PlateMap',
    'LibraryBuild',
    'Exclude',
]

metadata_columns_of_focus = [
    'UniqueId',
    'PlateMap',
    'Species',
    'Strain',
    'Bacterial_Source',
    'Ignore',
    'LibraryBuild',
]

# Adding globals

# Uses Picle dataframe (pickle_dataframe.pkl) instead of fetching from the web for tests speed up.
global PICKLE_DATAFRAME
PICKLE_DATAFRAME = False

global STORE_PICLE
STORE_PICLE = False

global UNIT_TEST
UNIT_TEST = False

global DEBUG_THREADS
DEBUG_THREADS = False

global PICKLE_FILEPATH
PICKLE_FILEPATH = 'pickle_dataframe/pickle_dataframe.pkl'

global PICKLE_UT_FULL_LIST_FILEPATH
PICKLE_UT_FULL_LIST_FILEPATH = 'static_data/pickle_ut_full_list.pkl'

global PICKLE_UT_FULL_FILEPATH
PICKLE_UT_FULL_FILEPATH = 'static_data/pickle_ut_full_dataframe.pkl'

global PICKLE_UT_PREPARED_FILEPATH
PICKLE_UT_PREPARED_FILEPATH = 'static_data/pickle_ut_prepared_dataframe.pkl'

global PICKLE_UT_FILTERED_FILEPATH
PICKLE_UT_FILTERED_FILEPATH = 'static_data/pickle_ut_filtered_dataframe.pkl'

global XLSX_FILENAME
XLSX_FILENAME = '-most_valuable_stocks.xlsx'

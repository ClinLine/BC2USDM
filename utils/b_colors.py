class BColors(str):
    '''Enum with acii values to change console text formatting'''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m' # Yellow
    FAIL = '\033[91m' # Red
    ENDC = '\033[0m' # End Color (White)
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
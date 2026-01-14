from uuid import uuid4 as guid
import numpy
import pandas

from models.USDM.code.code import Code


class LocalStorage:
    """ Class for managing local storage"""

    usdm_categories:numpy.Series
    usdm_biological_concepts:numpy.Series
    usdm_bc_properties:numpy.Series
    usdm_response_codes:numpy.Series
    usdm_codes:numpy.Series
    usdm_alias_codes:numpy.Series

    # packages:pandas.dataframe


    def __init__(self, files=None):
        ''' TODO:
        - Check if files exist
        - Read data from files
        - initialize Series
        - validate cache (use package?) : /mdr/bc/packages/2022-10-26/biomedicalconcepts/C49676",
        '''

        pass
    
    def __call__(self, *args, **kwds):
        pass

    def __new__(cls):
        pass

    @staticmethod
    def get_bcs_by_id(ids:list[guid]):
        raise NotImplementedError()
    
    @staticmethod
    def get_bcs_by_code(codes:list[Code]):
        raise NotImplementedError()
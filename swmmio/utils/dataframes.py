from swmmio.utils import text as txt
from swmmio.utils import functions as funcs
from swmmio.swmmio import rpt, inp
import pandas as pd
import os

def create_dataframeINP (inp, section='[CONDUITS]'):
    """
    given an inp object, create a dataframe of data in a given section
    """

    #find all the headers and their defs (section title with cleaned one-liner column headers)
    headerdefs = funcs.complete_inp_headers(inp.filePath)
    #create temp file with section isolated from inp file
    tempfilepath = txt.extract_section_from_inp(inp.filePath, section, headerdefs=headerdefs)
    if not tempfilepath:
        print 'header "{}" not found in "{}"'.format(section, inp.filePath)
        return None

    if headerdefs['headers'][section] == 'blob':
        #return the whole row, without specifc col headers
        df = pd.read_table(tempfilepath, delim_whitespace=False, comment=";")
    elif section == '[CURVES]' or section =='[TIMESERIES]':
        #return the whole row, without specifc col headers
        df = pd.read_table(tempfilepath, delim_whitespace=False, index_col=0, skiprows=[0])
    else:
        #this section header is recognized and will be organized into known columns
        headerlist = headerdefs['headers'][section].split()
        df = pd.read_table(tempfilepath, header=None, delim_whitespace=True, skiprows=[0],
                            comment=";", index_col=0, names = headerlist)
        #df.columns.names=[headerlist]
    os.remove(tempfilepath)

    #add new blank comment column
    df['Comment'] = ''


    return df

def create_dataframeRPT(rpt, section='Link Flow Summary'):
    """
    given an rpt object, create a dataframe of data in a given section
    """

    #find all the headers and their defs (section title with cleaned one-liner column headers)
    headerdefs = funcs.complete_rpt_headers(rpt.filePath)
    #create temp file with section isolated from rpt file
    tempfilepath = txt.extract_section_from_rpt(rpt.filePath, section, headerdefs=headerdefs)

    if not tempfilepath:
        print 'header "{}" not found in "{}"'.format(section, rpt.filePath)
        return None

    if headerdefs['headers'][section] == 'blob':
        #return the whole row, without specifc col headers
        df = pd.read_table(tempfilepath, delim_whitespace=False, comment=";")
    else:
        #this section header is recognized and will be organized into known columns
        headerlist = headerdefs['headers'][section].split()
        df = pd.read_table(tempfilepath, header=None, delim_whitespace=True, skiprows=[0],
                            comment=";", index_col=0, names = headerlist)
        #df.columns.names=[headerlist]
    os.remove(tempfilepath)

    #add new blank comment column
    df['Comment'] = ''


    return df

#!/usr/bin/python

""" A module to build the file paths of all database files needed for the other modules.
It first looks for the config file pathways.config, and if it cannot find that, then it
builds one itself.

Because people who stare at genomes a lot will already have their files stored somewhere
convenient for them, the construction of a config file that simply points to their
location for extraction by the other modules seems to make a lot of sense to me. This
also prevents absolute paths from having to be coded.
"""

import os, sys
import re
import time
import cPickle

from pkg_resources import resource_filename, resource_exists
#import pkgutil

def verbalise(arg1, *args):
    # define escape code: '\x1b[31m  %s  \x1b[0m'
    colordict = {'R':'\x1b[31m', 'G':'\x1b[32m',
         'Y':'\x1b[33m' ,'B':'\x1b[34m', 'M':'\x1b[35m' , 'C':'\x1b[36m' }
    if arg1 in colordict:
        argstring = " ".join([str(arg) for arg in args])
        if sys.stdout.isatty():
            color_code = colordict[arg1]
            end_color = '\x1b[0m'
        else:
            color_code = ""
            end_color = ""
    else:
        argstring = " ".join([arg1] + [str(arg) for arg in args])
        color_code = ""
        end_color = ""

    print "%s%s%s" % (color_code, argstring, end_color)

def check_verbose(v=True):
    "allow optional printing with color conversion capability!"
    global verbalise
    if v:
        verbalise = verbalise
    else:
        verbalise = lambda *a: None

    return verbalise

def read_pathways(config_file):
    """
    Extract the pathways of the filetypes specified in the config file.
    """
    pathway_dict = {}
    config_h = open( config_file, 'rb')
    # split each line into two (variable and path), if no comment symbol # is present:
    config_g = ( (line.split()[0], line.split()[1]) for line in config_h if re.search('#',line) == None)
    for fileid, pathway in config_g:
        if resource_exists('ortholotree', fileid + '.db'):
            pathway_dict[fileid] = resource_filename('ortholotree',
                                                os.path.join(['data/', fileid, '.db']))
        else:
            pathway_dict[fileid] = pathway
    return pathway_dict

def write_config(pathway_dict, config_file):
    config_h = open(config_file, 'w')
    for fileid in pathway_dict:
        config_h.write(" ".join([fileid,pathway_dict[fileid]]) + '\n')
    config_h.close()




##### FILE MANIPULATION #####
def pickle_jar(obj, fname):
    pklfile = ".".join([fname, 'pkl'])
    apicklefile = open(pklfile, 'wb')
    cPickle.dump(obj, apicklefile, -1)
    apicklefile.close()

def open_pickle_jar(fname):
    pklfile = ".".join([fname, 'pkl'])
    apicklefile = open(pklfile, 'rb')
    loaded_obj = cPickle.load(apicklefile)
    apicklefile.close()
    return loaded_obj



def file_block(filehandle,  block, number_of_blocks=1000):
    """
    This code adapted from:
    http://xor0110.wordpress.com/2013/04/13/how-to-read-a-chunk-of-lines-from-a-file-in-python/

    Written by Nic Werneck

    A generator that splits a file into blocks and iterates
    over the lines of one of the blocks.

    usage:
    filehandle = open(filename)
    number_of_chunks = 100
    for chunk_number in range(number_of_chunks):
        for line in file_block(filehandle, number_of_chunks, chunk_number):
            process(line)
    """


    assert 0 <= block and block < number_of_blocks
    assert 0 < number_of_blocks

    filehandle.seek(0,2)
    file_size = filehandle.tell()

    ini = file_size * block / number_of_blocks
    end = file_size * (1 + block) / number_of_blocks

    if ini <= 0:
        filehandle.seek(0)
    else:
        filehandle.seek(ini-1)
        filehandle.readline()

    while filehandle.tell() < end:
        yield filehandle.readline()

def check_overwrite(message="File exists! Do you want to overwrite? [Y/N]\n"):
    answer = raw_input(message)
    if answer.upper() in ["Y", "YES"]:
        return True
    else:
        return False

def create_log(args, outdir=None, outname='results'):
    ## create output folder and log file of arguments:
    timestamp = time.strftime("%b%d_%H.%M")
    if outdir:
        newfolder = os.path.realpath(outdir)
        if os.path.exists(newfolder) is False:  # check to see if folder already exists...
            os.mkdir(newfolder)
        filename = newfolder + '/' + outname + '.' + timestamp + ".log"
        if os.path.exists(filename) is True: # ask to overwrite:
            if check_overwrite():
                pass
            else:
                exit()
    else:
        root_dir = os.getcwd()
        newfolder = root_dir + "/" + outname + "." + timestamp
        if os.path.exists(newfolder) is False:  # check to see if folder already exists...
            os.mkdir(newfolder)
        filename = newfolder + '/' + outname + '.' + timestamp + ".log"
        if os.path.exists(filename) is True: # ask to overwrite:
            if check_overwrite():
                pass
            else:
                exit()
        filename = newfolder + "/" + outname + "." + timestamp + ".log"

    log_h = open(filename, 'w')
    log_h.write( "File created on %s\n" % (timestamp) )
    log_h.write( "Program called from %s\n" % (os.getcwd()) )
    log_h.write( "%s\n\n" % (' '.join(sys.argv)) )
    for arg in str(args)[10:-1].split():
        log_h.write( "%s\n" % (arg) )
    log_h.close()
    return filename

def make_a_list(listlikeobj, col_num=0, readfile=True, sep='\s,'):
    """
    given a path, list, dictionary or string, convert into a list of genes.
    col_num specifies the column from which to extract the gene list from in a file.

    returns a list
    """

    if type(listlikeobj) is list:
        thelist = listlikeobj
    elif type(listlikeobj) is dict:
        thelist = listlikeobj.keys()
        verbalise("R", "object was a dictionary, returning keys only as list")
    elif type(listlikeobj) is str:
        if os.path.exists(listlikeobj) and readfile: # can turn off file reading
            genefile_h = open(listlikeobj, 'rb')
            thelist = []
            for line in genefile_h:
                if len(line) == 0:
                    continue
                cols = line.split()
                if len(cols) >= col_num:
                    thelist.append(cols[col_num])
        else:
            thelist = re.findall(r'[^' + sep + ']+', listlikeobj)
    else:
        thelist = []

    return thelist


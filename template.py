#! /usr/bin/env python
"""
A wrapper to identify, extract, align and phylogenise a target gene. The primary purpose
of this module is for a user to confirm orthology of their gene, not to understand in
detail the phylogenetic relationships between all closely related proteins.
"""

import argparse
import os
import tempfile

import config


############################################################################

def define_arguments():
    parser = argparse.ArgumentParser(description=
            "A module to perform a variety of gene term related analyses")
    ### input options ###
    group1 = parser.add_argument_group('input and logging options')
    group1.add_argument("-q", "--quiet", action='store_true',default=False,
                        help="print fewer messages and output details")
    group1.add_argument("-o", "--output", type=str, default='genematch.out',
                        help="specify the filename to save results to")
    group1.add_argument("-d", "--directory", type=str,
                        help="specify the directory to save results to")
    group1.add_argument("--display_on", action='store_true',default=False,
                        help="display graph results (eg for p value calculation)")


    # data file options:
    group2 = parser.add_argument_group('data file options')
    group2.add_argument("-f", "--fasta", type=str, nargs='+',
                        help="""provide at least one fasta file""")

    # analysis options:
    group3 = parser.add_argument_group('analysis options')
    group3.add_argument("-B", "--do_it", action='store_true',
                        help="""does something""")
    group3.add_argument("-c", "--int_with_default", type=int, default=2,
                        help="""get an integer [default = 2]""")
    group3.add_argument("-t", "--float_w_default", type=float, default=0.5,
                        help="""get a float [default = 0.5]""")
    group3.add_argument("-x", "--string", type=str,
                        help="""get a string""")
    return parser



############################################################################

if __name__ == '__main__':
    parser = define_arguments()
    args = parser.parse_args()

    verbalise = config.check_verbose(not(args.quiet))
    logfile = config.create_log(args, outdir=args.directory, outname=args.output)

    temp_dir = tempfile.mkdtemp()

    ############################

    # INSERT CODE HERE         #

    ############################


    # clean up temp files and directory
    for file in temp_dir:
        os.remove(file)

    os.rmdir(temp_dir)  # dir must be empty to be removed!

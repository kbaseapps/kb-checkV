# -*- coding: utf-8 -*-
#BEGIN_HEADER
# The header block is where all import statments should live
from Bio import SeqIO
import logging
import os
import pandas as pd
from pprint import pformat
import subprocess
import uuid
import zipfile


from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.DataFileUtilClient import DataFileUtil
from kb_checkV import run_kb_checkv, generate_output_file_list, generate_html_report, generate_template_report
#END_HEADER


class kb_checkV:
    '''
    Module Name:
    kb_checkV

    Module Description:
    A KBase module: kb_checkV
This sample module contains one small method that filters contigs.
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/kbaseapps/kb-checkV.git"
    GIT_COMMIT_HASH = "69518e3d238baf8dae5a4751ec0684494224a28f"

    #BEGIN_CLASS_HEADER
    # Class variables and functions can be defined in this block
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        
        # Any configuration parameters that are important should be parsed and
        # saved in the constructor.
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        self.dfu = DataFileUtil(self.callback_url)
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_kb_checkV(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_kb_checkV

        # test
        # Print statements to stdout/stderr are captured and available as the App log
        logging.info('Starting run_kb_checkV function. Params=' + pformat(params))

        # Step 1 - Parse/examine the parameters and catch any errors
        # It is important to check that parameters exist and are defined, and that nice error
        # messages are returned to users.  Parameter values go through basic validation when
        # defined in a Narrative App, but advanced users or other SDK developers can call
        # this function directly, so validation is still important.
        logging.info('Validating parameters.')
        if 'workspace_name' not in params:
            raise ValueError('Parameter workspace_name is not set in input arguments')
        workspace_name = params['workspace_name']
        # if 'assembly_input_ref' not in params:
        #     raise ValueError('Parameter assembly_input_ref is not set in input arguments')
        assembly_input_ref = params['assembly_input_ref']

        # Step 2 - Download the input data as a Fasta and
        # We can use the AssemblyUtils module to download a FASTA file from our Assembly data object.
        # The return object gives us the path to the file that was created.
        logging.info('Downloading Assembly data as a Fasta file.')
        assemblyUtil = AssemblyUtil(self.callback_url)
        fasta_file = assemblyUtil.get_assembly_as_fasta({'ref': assembly_input_ref})

        # Step 3 - Actually perform the filter operation, saving the good contigs to a new fasta file.
        # We can use BioPython to parse the Fasta file and build and save the output to a file.
        logging.info("Now running checkv end_to_end command")
        output_dir = "/opt/work/outputdir"
        logging.info("CheckV is running: ")
        process = run_kb_checkv(output_dir, fasta_file['path'])

        # Step 4 - Save the new Assembly back to the system

        kbase_report_client = KBaseReport(self.callback_url, service_ver='dev')
        # HTML report
        logging.info('start generating html files')
        html_report = generate_template_report(output_dir, self.shared_folder, kbase_report_client)

        # Step 5 - Build a Report and return

        report_params = {'message': '',
                         'workspace_name': params.get('workspace_name'),
                         'html_links': html_report,
                         'direct_html_link_index': 0,
                         'html_window_height': 333,
                         'report_object_name': 'kb_checkv_report_' + str(uuid.uuid4())}

        report_info = kbase_report_client.create_extended_report(report_params)

        # # STEP 6: contruct the output to send back

        output = {'report_name': report_info['name'],
                  'report_ref': report_info['ref'],
                  'result_directory': output_dir,
                  }

        #END run_kb_checkV
        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_kb_checkV return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]

# -*- coding: utf-8 -*-
import csv
import os
import subprocess
import time
import unittest

from configparser import ConfigParser

from kb_checkV.kb_checkVImpl import kb_checkV
from kb_checkV.kb_checkVServer import MethodContext
from kb_checkV.authclient import KBaseAuth as _KBaseAuth

from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.WorkspaceClient import Workspace

output_dir = "/opt/work/outputdir"
input_file_path = "/opt/work/checkv/test/test_sequences.fna"
ground_truth_path = "/opt/work/checkv/test/ground_truth"

class kb_checkVTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        time.sleep(5)
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_checkV'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_checkV',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = kb_checkV(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa
        cls.prepareTestData()

    @classmethod
    def prepareTestData(cls):
        """This function creates an assembly object for testing"""
        fasta_content = '>seq1 something soemthing asdf\n' \
                        'agcttttcat\n' \
                        '>seq2\n' \
                        'agctt\n' \
                        '>seq3\n' \
                        'agcttttcatgg'

        filename = os.path.join(cls.scratch, 'test1.fasta')
        with open(filename, 'w') as f:
            f.write(fasta_content)
        assemblyUtil = AssemblyUtil(cls.callback_url)
        cls.assembly_ref = assemblyUtil.save_assembly_from_fasta({
            'file': {'path': filename},
            'workspace_name': cls.wsName,
            'assembly_name': 'TestAssembly'
        })

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa

    def test_run_kb_checkV_ok(self):
        # call your implementation
        ret = self.serviceImpl.run_kb_checkV(self.ctx,
                                                {'workspace_name': self.wsName,
                                                 'assembly_input_ref': self.assembly_ref,
                                                 })
        # Validate the returned data
        self.assertEqual(1,1)



    def test_run_kb_checkV_checkv_help(self):

        process = subprocess.run(['checkv', '--help'],
                                 stdout=subprocess.PIPE)
        # print(process.stdout.decode("utf-8"))
        self.assertEqual(process.returncode, 0)


    def test_checkv_end_to_end(self):
        # setup environment
        os.environ['CHECKVDB'] = "/data/checkv-db-v0.6"

        # Run command
        process = subprocess.run(['checkv', 'end_to_end', input_file_path, output_dir, '-t', '16'],
        # process = subprocess.run(['ls', '-halF', '/opt/work/checkv'],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
        # print("This is the output: ", process.stdout.decode("utf-8"))
        self.assertEqual(process.returncode, 0)

        # Compare files with
        files = ['complete_genomes.tsv', 'completeness.tsv', 'contamination.tsv', 'quality_summary.tsv']
        for file in files:
            truth_file_path = os.path.join(ground_truth_path, file)
            gen_file_path = os.path.join(output_dir, file)
            self.assertTrue(gen_file_path)
            with open(gen_file_path) as gen_f:
                gen_file = csv.reader(gen_f, delimiter="\t", quotechar='"')
                gen_header = next(gen_file)
            with open(truth_file_path) as truth_f:
                truth_file = csv.reader(truth_f, delimiter="\t", quotechar='"')
                truth_header = next(truth_file)
            self.assertEqual(gen_header, truth_header)

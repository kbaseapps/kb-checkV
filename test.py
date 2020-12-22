import csv
from os import path
import os, shutil
import subprocess
import unittest

output_dir = "/Users/yangzm/KBase/checkV/outputdir_test"



class MyTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        # clear outputdir
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def test_run(self):
        input_file_path = "/Users/yangzm/KBase/checkV/checkv/test/test_sequences.fna"

        process = subprocess.run(['checkv', 'end_to_end', input_file_path, output_dir, '-t', '16'],
                                 stdout=subprocess.PIPE)
        print(process.stdout.decode("utf-8"))
        self.assertEqual(process.returncode, 0)

        self.assertTrue(path.exists(path.join(output_dir, 'complete_genomes.tsv')))
        self.assertTrue(path.exists(path.join(output_dir, 'completeness.tsv')))
        self.assertTrue(path.exists(path.join(output_dir, 'contamination.tsv')))
        self.assertTrue(path.exists(path.join(output_dir, 'quality_summary.tsv')))


    def test_column_num(self):
        complete_genomes_ncol, completeness_ncol, contamination_ncol, quality_summary_ncol = 11, 15, 14, 14
        ncols = [complete_genomes_ncol, completeness_ncol, contamination_ncol, quality_summary_ncol]
        files = ['complete_genomes.tsv', 'completeness.tsv', 'contamination.tsv', 'quality_summary.tsv']
        for i in range(len(files)):
            with open("outputdir/" + files[i]) as f:
                rd = csv.reader(f, delimiter="\t", quotechar='"')
                ncol = len(next(rd))
                self.assertEqual(ncol, ncols[i])


    def test_print(self):
        print("Test finished.")






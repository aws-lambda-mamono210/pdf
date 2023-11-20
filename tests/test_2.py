import boto3
import shutil
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tempfile
from PyPDF2 import PdfWriter
from PyPDF2 import PdfReader
from common_modules.pdf_merger.pdf_merger import merge_pdfs_in_directory
from common_modules.pdf_utils.pdf_utils import create_pdf_with_text
from handler import handler

class TestHandler(unittest.TestCase):

    def setUp(self):
        print("Setup Proccess")
        # Setup necessary variables for the tests
        self.bucket_name = 'mamono210'
        self.s3_folder_name = 'aws/lambda/pdf/tests/2/'
        self.region_name = 'ap-northeast-1'
        self.download_directory = 'test_2_downloaded_files'
        self.output_filename = 'test_2_output_with_page_numbers.pdf'
        self.merged_filename = 'test_2_merged_output.pdf'
        self.s3_object_name = 'aws/lambda/pdf/tests/2/test_2_merged_output.pdf'


    def test_handler(self):
        # Test the handler function
        handler(self.bucket_name, self.s3_folder_name, self.region_name, self.download_directory, self.output_filename, self.merged_filename, self.s3_object_name)

        # Check if the output file is created
        self.assertTrue(os.path.exists(self.output_filename))

        # Check if the merged file is created
        self.assertTrue(os.path.exists(self.merged_filename))

        # Additional assertions can be added here to verify the content of the output files

    def tearDown(self):
        save_dir = "artifacts"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        if os.path.exists(self.output_filename):
            # Move the output file to the 'artifacts' directory
            shutil.move(self.output_filename, os.path.join(save_dir, self.output_filename))

        if os.path.exists(self.merged_filename):
            # Move the merged file to the 'artifacts' directory
            shutil.move(self.merged_filename, os.path.join(save_dir, self.merged_filename))

        if os.path.exists(self.download_directory):
            shutil.rmtree(self.download_directory)

if __name__ == '__main__':
    unittest.main()

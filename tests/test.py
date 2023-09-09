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
        # Setup necessary variables for the tests
        self.bucket_name = 'mamono210'
        self.object_keys = ['aws/lambda/pdf/test_file1.pdf', 'aws/lambda/pdf/test_file2.pdf']  # Replace with your test file names
        self.output_directory = 'test_downloaded_files'
        self.output_filename = 'test_output_with_page_numbers.pdf'
        self.merged_filename = 'test_merged_output.pdf'

        os.makedirs(os.path.join(self.output_directory, 'aws/lambda/pdf'), exist_ok=True)

        # Create test PDF files
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        # Step 1: Create test files locally
        create_pdf_with_text("Test Content for File 1", os.path.join(self.output_directory, 'test_file1.pdf'))
        create_pdf_with_text("Test Content for File 2", os.path.join(self.output_directory, 'test_file2.pdf'))

        # Step 2: Upload test files to S3
        s3_client = boto3.client('s3')
        s3_client.upload_file(os.path.join(self.output_directory, 'test_file1.pdf'), self.bucket_name, self.object_keys[0])
        s3_client.upload_file(os.path.join(self.output_directory, 'test_file2.pdf'), self.bucket_name, self.object_keys[1])

    def test_handler(self):
        # Test the handler function
        handler(self.bucket_name, self.object_keys, self.output_directory, self.output_filename, self.merged_filename)

        # Check if the output file is created
        self.assertTrue(os.path.exists(self.output_filename))

        # Check if the merged file is created
        self.assertTrue(os.path.exists(self.merged_filename))

        # Additional assertions can be added here to verify the content of the output files

    def tearDown(self):
        # Clean up files created during the test
        if os.path.exists(self.output_filename):
            os.remove(self.output_filename)

        if os.path.exists(self.merged_filename):
            os.remove(self.merged_filename)

        if os.path.exists(self.output_directory):
           shutil.rmtree(self.output_directory)

if __name__ == '__main__':
    unittest.main()

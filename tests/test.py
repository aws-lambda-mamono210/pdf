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
        self.output_directory = 'test_downloaded_files'
        self.output_filename = 'test_output_with_page_numbers.pdf'
        self.merged_filename = 'test_merged_output.pdf'
        self.s3_object_name = 'aws/lambda/pdf/test_merged_output.pdf'

        # 10個のキーを生成します
        self.object_keys = [f'aws/lambda/pdf/test_file{i}.pdf' for i in range(1, 11)]

        os.makedirs(os.path.join(self.output_directory, 'aws/lambda/pdf'), exist_ok=True)

        # Create test PDF files
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        s3_client = boto3.client('s3')

        # Step 1 and Step 2: Create test files locally and Upload them to S3
        for i in range(1, 11):
            file_name = f"{str(i).zfill(2)} test_file{i}.pdf"
            file_path = os.path.join(self.output_directory, file_name)

            # Step 1: Create test files locally
            create_pdf_with_text(f"Test Content for File {i}", file_path)

            # Step 2: Upload test files to S3
            s3_client.upload_file(file_path, self.bucket_name, self.object_keys[i - 1])


    def test_handler(self):
        # Test the handler function
        handler(self.bucket_name, self.object_keys, self.output_directory, self.output_filename, self.merged_filename, self.s3_object_name)

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

        if os.path.exists(self.output_directory):
            shutil.rmtree(self.output_directory)

if __name__ == '__main__':
    unittest.main()

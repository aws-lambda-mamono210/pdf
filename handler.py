import os
from common_modules.pdf_merger.pdf_merger import merge_pdfs_in_directory
from common_modules.pdf_pager.pdf_pager import add_page_numbers
from common_modules.s3_utils.s3_utils import S3Utils

def handler(bucket_name, object_keys, output_directory, output_filename, merged_filename, s3_object_name):
    # Step 1: Initialize the S3 client
    s3_client = S3Utils(bucket_name)

    # Step 2: Download the objects
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for object_key in object_keys:
        destination_path = os.path.join(output_directory, object_key)
        s3_client.download_file(object_key, destination_path)

    # Step 3: Merge the downloaded files
    merge_pdfs_in_directory(output_directory, merged_filename)

    # Step 4: Add page numbers to the merged file
    add_page_numbers(merged_filename, output_filename)

    # Step 5: Upload the merged file to S3
    s3_client.upload_file(output_filename, s3_object_name)

    print("Process completed successfully!")

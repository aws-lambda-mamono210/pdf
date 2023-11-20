import boto3
import os
import re
from pathlib import Path
from common_modules.pdf_merger.pdf_merger import merge_pdfs_in_directory
from common_modules.pdf_pager.pdf_pager import add_page_numbers

def handler(bucket_name, s3_folder_name, region_name, download_directory, output_filename, merged_filename, s3_object_name):
    # Step 1: Initialize the S3 client
    print("Step 1: Initialize the S3 client.")
    s3 = s3 = boto3.client(
        's3',
        region_name=region_name
    )

    # Step 2: Download the objects
    print("Step 2: Download the objects.\n")

    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    print(f"Create {download_directory}.")

    # List files in a specific folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_folder_name)

    # Download files that match the pattern
    pattern = r'^\d{2}.*\.pdf$'

    if 'Contents' in response:
        for file in response['Contents']:
            file_name = file['Key']
            local_file_name = file_name.split('/')[-1]  # Set the local file name
            if re.match(pattern, local_file_name):
                destination_path = os.path.join(download_directory, local_file_name)
                s3.download_file(bucket_name, file_name, destination_path)
                print(f'Downloaded {file_name} to {destination_path}')

    print("Download completed.\n")

    # Step 3: Merge the downloaded files
    print("Step 3: Merge the downloaded files.")
    merge_pdfs_in_directory(download_directory, merged_filename)

    # Step 4: Add page numbers to the merged file
    print("Step 4: Add page numbers to the merged file.")
    add_page_numbers(merged_filename, output_filename)

    # Step 5: Upload the merged file to S3
    print("Step 5: Upload the merged file to S3.")
    s3.upload_file(output_filename, bucket_name, s3_object_name)

    print("Process completed successfully!")

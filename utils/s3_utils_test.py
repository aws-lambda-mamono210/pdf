import boto3
import unittest
from moto import mock_s3
from s3_utils import S3Utils

@mock_s3
class TestS3Utils(unittest.TestCase):

    def setUp(self):
        self.bucket_name = 'test-bucket'
        region_name = "ap-northeast-1"
        self.utils = S3Utils(self.bucket_name, region_name)
        self.utils.s3 = boto3.client('s3', region_name=region_name)

    def tearDown(self):
        try:
            bucket_objects = self.utils.s3.list_objects(Bucket=self.bucket_name)
            for obj in bucket_objects.get('Contents', []):
                self.utils.s3.delete_object(Bucket=self.bucket_name, Key=obj['Key'])
            self.utils.s3.delete_bucket(Bucket=self.bucket_name)
        except:
            pass

    def test_bucket_creation(self):
        self.utils.create_bucket()
        response = self.utils.s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        self.assertIn(self.bucket_name, buckets)

    def test_bucket_deletion(self):
        self.utils.create_bucket()
        self.utils.delete_bucket()
        response = self.utils.s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        self.assertNotIn(self.bucket_name, buckets)

    def test_file_upload_and_list(self):
        self.utils.create_bucket()
        filename = 'test.txt'
        content = 'Hello, World!'
        with open(filename, 'w') as f:
            f.write(content)

        self.utils.upload_file(filename, 'destination_test.txt')
        files = self.utils.list_files()
        self.assertIn('destination_test.txt', files)

    def test_file_download(self):
        self.utils.create_bucket()
        filename = 'test.txt'
        content = 'Hello, World!'
        with open(filename, 'w') as f:
            f.write(content)
        self.utils.upload_file(filename, 'destination_test.txt')

        source_name = 'destination_test.txt'
        dest_path = 'downloaded_test.txt'
        self.utils.download_file(source_name, dest_path)

        with open(dest_path, 'r') as f:
            downloaded_content = f.read()

        self.assertEqual(downloaded_content, 'Hello, World!')

    def test_file_deletion(self):
        self.utils.create_bucket()
        self.utils.delete_file('destination_test.txt')
        files = self.utils.list_files()
        self.assertNotIn('destination_test.txt', files)

if __name__ == "__main__":
    unittest.main()

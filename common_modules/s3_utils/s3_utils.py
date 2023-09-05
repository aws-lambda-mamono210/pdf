import boto3

class S3Utils:
    def __init__(self, bucket_name, region_name='ap-northeast-1'):
        self.s3 = boto3.client('s3', region_name=region_name)
        self.bucket_name = bucket_name
        self.region_name = region_name

    def bucket_exists(self):
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            return True
        except:
            return False

    def create_bucket(self):
        if not self.bucket_exists():
            if self.region_name == 'us-east-1':
                self.s3.create_bucket(Bucket=self.bucket_name)
            else:
                self.s3.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': self.region_name}
                )

    def upload_file(self, filename, destination_name):
        self.s3.upload_file(filename, self.bucket_name, destination_name)
        print(f"Uploaded '{filename}' to '{destination_name}' in bucket '{self.bucket_name}'.")

    def download_file(self, source_name, destination_path):
        self.s3.download_file(self.bucket_name, source_name, destination_path)
        print(f"Downloaded '{source_name}' from bucket '{self.bucket_name}' to '{destination_path}'.")

    def list_files(self):
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        files = [obj['Key'] for obj in response.get('Contents', [])]
        for file in files:
            print(file)
        return files

    def delete_file(self, filename):
        self.s3.delete_object(Bucket=self.bucket_name, Key=filename)
        print(f"Deleted '{filename}' from bucket '{self.bucket_name}'.")

    def delete_bucket(self):
        self.s3.delete_bucket(Bucket=self.bucket_name)
        print(f"Bucket '{self.bucket_name}' deleted.")

# CloudFunction 백업용

''' # CloudFunction
트리거 유형: Cloud Storage
Event type: 완료/생성
버킷: kpu-capstone-test.appspot.com
version: Python 3.7
'''

''' # requirement.txt
# Function dependencies, for example:
# package>=version

google-cloud-storage==1.16.1
'''

from google.cloud import storage

# download from bucket to tmp
def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


def main(event, context):
    file_path = event['name'].split('/')

    if (file_path[0] == 'audio'):
        # 호출
        download_blob(
            bucket_name="kpu-capstone-test.appspot.com",
            source_blob_name=event['name'],
            destination_file_name="/tmp/" + file_path[-1]
        )

        download_blob(
            bucket_name="kpu-capstone-test.appspot.com",
            source_blob_name='model/' + file_path[1] + '/model.h5',
            destination_file_name="/tmp/model.h5"
        )

        # 호출
        upload_blob(
            bucket_name="kpu-capstone-test.appspot.com",
            source_file_name="/tmp/model.h5",
            destination_blob_name='model/' + file_path[1] + '/model.h5'
        )

        print('upload success')
    else:
        print(file_path[0])
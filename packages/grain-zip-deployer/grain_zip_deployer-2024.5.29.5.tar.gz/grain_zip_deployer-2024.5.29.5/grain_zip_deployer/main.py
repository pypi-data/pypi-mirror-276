import zipfile
import os
from io import BytesIO
import subprocess
from grain_zip_deployer import settings
import argparse
import fnmatch

from pathlib import Path

from google.cloud import storage
from google.oauth2.credentials import Credentials


__VERSION__ = 0.1

def init_argparse():

    # argument parser to parse arguments from the command line

    parser = argparse.ArgumentParser(
            description='Deploy sourcecode to a Google Cloud storage bucket.',
            allow_abbrev=False
    )

    parser.add_argument('-n', '--name', help='The filename of the zip archive file', required=True)
    parser.add_argument('-f', '--folder', help='The path of the sourcecode folder, current directory by default')

    # default behaviour is that the zip archive will only be created in the current directory.
    # when specifying the parameters below, the archive will be uploaded to the bucket, but not retained on disk
    parser.add_argument('-u', '--upload', help='Also upload to the bucket', action='store_true', default=False)
    parser.add_argument('-b', '--bucket', help='The name of the bucket')
    parser.add_argument('-p', '--project_id', help='The project-id of the project that contains the bucket')
    
    

    return parser

def upload_to_bucket(bucket_name,
                     project_id,
                     file_name,
                     archive_stream):

    # get short-lived (1 hour) access token and create credentials
    access_token = get_access_token()
    credentials = Credentials(token=access_token)

    # Initialize the client with the credentials and the project
    client = storage.client.Client(project=project_id, credentials=credentials)

    bucket = client.get_bucket(bucket_name)

    blob_new = bucket.blob(file_name)
    blob_new.upload_from_string(archive_stream.getvalue())

def get_access_token():

    # get a temporary access token from the command line that is valid for one hour
    result = subprocess.run(
            ['gcloud', 'auth', 'print-access-token'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
            check=True
        )
        
    # The access token will be in the stdout
    return result.stdout.strip()


def read_gcloudignore(file_path):

    ignore_patterns = []

    try:

        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.append(line)

    except FileNotFoundError:

        print(f'No ignore file found at {file_path}.')

    return ignore_patterns


def should_ignore(file_path, 
                  ignore_patterns):
    
    # match patterns in ignore file with file paths, to see if they should be ignored
    for pattern in ignore_patterns:

        if fnmatch.fnmatch(file_path, pattern) or fnmatch.fnmatch(os.path.basename(file_path), pattern):
            return True
        
    return False


def zipdir(source_folder, 
           file_name):

    # open a bytes stream to add the zip archive to
    archive_stream = BytesIO()

    # get the ignore patters and at the zip file itself
    ignore_patterns = read_gcloudignore(settings.DEFAULT_GCLOUD_IGNORE_FILE) + [file_name] + [settings.DEFAULT_GCLOUD_IGNORE_FILE]

    # with zipfile.ZipFile(archive_stream, 'w') as zipfile_new:
    with zipfile.ZipFile(archive_stream, 'w', zipfile.ZIP_DEFLATED) as zipfile_new:

        # walk through the source folder directory
        for root, dirs, files in os.walk(source_folder):

            for file in files:
                
                # determine the full path of each file
                file_path = os.path.join(root, file)
                
                # determine the path relative to the source folder
                # these are used to match against the ignore patterns
                rel_path = os.path.relpath(file_path, source_folder)

                if not should_ignore(rel_path, ignore_patterns=ignore_patterns):
                    
                    # if the file should not be ignored based on the ignore patterns
                    # we add it to the zip file

                    zipfile_new.write(file_path, rel_path)

    return archive_stream


def write_archive_file(file_name, archive_stream):

    value = archive_stream.getvalue()

    with open(file_name, 'wb') as f:
        f.write(value)
        
        
def main():

    parser = init_argparse()
    args = parser.parse_args()
    
    archive_name = args.name
    
    # get the directory with source files. Current working directory by default
    if not args.folder is None:
        source_dir = args.folder
    else:
        source_dir = Path.cwd()

    if args.upload:

        # when uploading, the bucket is mandatory
        if args.bucket is None:
            raise ValueError('No bucket given')
        bucket = args.bucket

        # wehen uploading, a gcloud project is mandatory
        if args.project_id is None:
            raise ValueError('No project given')
        project_id=args.project_id

    else:

        bucket = None
        project_id=None

    archive_stream = zipdir(source_dir, file_name=archive_name)

    if not args.upload:
    
        write_archive_file(file_name=archive_name, archive_stream=archive_stream)

    else:

        upload_to_bucket(bucket_name=bucket,
                         project_id=project_id,
                         file_name=archive_name,
                         archive_stream=archive_stream)

if __name__ == '__main__':
    main()
    


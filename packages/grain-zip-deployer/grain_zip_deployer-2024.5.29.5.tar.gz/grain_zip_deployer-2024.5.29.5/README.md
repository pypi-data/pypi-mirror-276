# DataCurrent - Zip Deployer

This package is meant to easily create a zipfile from a existing source-folder and upload it to a gcloud bucket

## Installation

```
pip install grain_zip_deployer --upgrade
```

## Usage

When running the script it will look for a `.gcloudignore` file to determine which file to include
in the archive. This is mandatory, but can be an empty file. It is recommended to the archive creation
locally and see if no unexpected files are included in the archive.

To create a zipfile locally, run the following command from the source-code folder.
The file will be created in that same folder. Nothing will be uploaded

```
grain_upload_zip -n my_zip_archive_name.zip 
```

To actually upload to a bucket, you do

```
grain_upload_zip -n path/in/thebucket/my_zip_archive_name.zip -b my_bucket_name -p my_gcloud_project_id -u
```


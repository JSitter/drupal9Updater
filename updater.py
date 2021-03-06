#!/usr/bin/env python3
from optparse import OptionParser
import os
import os.path as path
import requests
import shutil
import sys
import tarfile
import urllib.request
import zipfile

current_version_url = 'https://www.drupal.org/download-latest/tar.gz'
home_directory = os.path.dirname(os.path.realpath(__file__))
temp_dir = './.tempdir'
zipped_package_location = None

forbidden_folders = {'sites', 'modules', 'profiles', 'themes'}
forbidden_files = {'.htaccess'}

def check_temp_dir():
    if not path.exists(temp_dir):
        os.mkdir(temp_dir)

def replace_item(source, destination):
    if path.isdir(destination):
        remove_directory(destination)
    else:
        remove_file(destination)
    shutil.move(source, destination)

def update_file(temp_location, file, destination, replace=False):
    file_destination = "{}/{}".format(destination, file)
    if not path.exists(file_destination):
        shutil.move("{}/{}".format(temp_location, file), destination)
    elif replace:
        replace_item("{}/{}".format(temp_location, file), "{}/{}".format(destination, file))
        print("Replaced {}.".format(file))
    else:
        if file in forbidden_folders or file in forbidden_files:
            print("Skipping {}. Already exists.".format(file))
        else:
            try:
                replace_item("{}/{}".format(temp_location, file), "{}/{}".format(destination, file))
                print("Replaced {}.".format(file))
            except:
                print("{} locked.")

def remove_file(source):
    print("remove file: {}".format(source))
    os.remove(source)

def remove_directory(source):
    print("Remove directory {}".format(source))
    shutil.rmtree(source)

def unpack_zip_into(source, destination, replace=False):
    zipReference = zipfile.ZipFile(source, 'r')
    allfiles = zipReference.namelist()
    temp_source_dir = "{}/{}".format(temp_dir, allfiles[0])
    check_temp_dir()
    
    zipReference = zipfile.ZipFile(source, 'r')
    zipReference.extractall(temp_dir)
    files = os.listdir(temp_source_dir)

    for file in files:
        update_file(temp_source_dir, file, destination, replace)
        
    shutil.rmtree(temp_source_dir)
    zipReference.close()
    print("Done")

def unpack_gz_into(source, destination, replace=False):
    tar = tarfile.open(source, 'r:gz')
    allfiles = tar.getnames()
    temp_source_dir = "{}/{}".format(temp_dir, allfiles[0])

    if not path.exists(temp_dir):
        os.mkdir(temp_dir)
    
    tarball = tarfile.open(source, 'r:gz')
    tarball.extractall(path=temp_dir)
    files = os.listdir(temp_source_dir)

    for file in files:
        update_file(temp_source_dir, file, destination, replace)
    shutil.rmtree(temp_source_dir)
    print("Done")

if __name__ == "__main__":
    usage = "usage: %prog [options] drupal_installation_location"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--download",
                        help="Download update from url.",
                        dest="download_url")

    parser.add_option("-l", "--local",
                        help="Path to compressed Drupal package.",
                        dest="local_path")

    parser.add_option("-f", "--force",
                        help="Force replacement of all files.",
                        dest="force")

    (options, args) = parser.parse_args()
    home_directory = path.dirname(path.realpath(__file__))

    if args[0][-1] == '/':
        drupal_install_location = args[0][:-1]
    else:
        drupal_install_location = args[0]

    if len(args) > 0:
        drupal_project_directory = home_directory+"/"+args[0]
    else:
        raise Exception("Error: Drupal project not provided.")

    if options.local_path is not None:
        if not path.exists("{}/{}".format(home_directory, options.local_path)):
            raise Exception("Error: Project {} doesn't exist".format(options.local_path))
        else:
            zipped_package_location = "{}/{}".format(home_directory, options.local_path)
            print("Updating from {}".format(zipped_package_location))

    elif options.download_url is not None:
        # Download zipped project
        current_version_url = options.download_url
    else:
        raise Exception("Error: Zipped Drupal project or download URL must be provided")

    if tarfile.is_tarfile(zipped_package_location):
        unpack_gz_into(zipped_package_location, args[0])

    elif zipfile.is_zipfile(zipped_package_location):
        unpack_zip_into(zipped_package_location, args[0])

    else:
        raise Exception("Not a valid update package.")
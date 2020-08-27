#!/usr/bin/env python3
from optparse import OptionParser
import os
import os.path as path
import shutil
import sys
import tarfile
import urllib.request
import zipfile

current_version_url = 'https://www.drupal.org/download-latest/tar.gz'
home_directory = os.path.dirname(os.path.realpath(__file__))
temp_dir = './tempdir'
zipped_package_location = None

forbidden_folders = {'sites', 'modules', 'profiles', 'themes', 'vendor'}

def check_temp_dir():
    if not path.exists(temp_dir):
        os.mkdir(temp_dir)

def replace_item(source, destination):
    if path.isdir(destination):
        remove_directory(destination)
    else:
        remove_file(destination)
    shutil.move(source, destination)

def unpack_zip_into(source, destination, replace=False):
    zipReference = zipfile.ZipFile(source, 'r')
    allfiles = zipReference.namelist()
    temp_source_dir = "{}/{}".format(temp_dir, allfiles[0])
    check_temp_dir()
    
    zipReference = zipfile.ZipFile(source, 'r')
    zipReference.extractall(temp_dir)
    files = os.listdir(temp_source_dir)

    for file in files:
        file_destination = "{}/{}".format(destination, file)
        if not path.exists(file_destination):
            shutil.move("{}/{}".format(temp_source_dir, file), destination)
        elif replace:
            replace_item("{}/{}".format(temp_source_dir, file), "{}/{}".format(destination, file))
            print("Replaced {}.".format(file))
        else:
            print("Skipping {}. Already Exists. ".format(file))
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
        file_destination = "{}/{}".format(destination, file)
        if not path.exists(file_destination):
            shutil.move("{}/{}".format(temp_source_dir, file), destination)
        elif replace:
            replace_item("{}/{}".format(temp_source_dir, file), "{}/{}".format(destination, file))
            print("Replaced {}.".format(file))
        else:
            print("Skipping {}. Already exists.".format(file))
    shutil.rmtree(temp_source_dir)
    print("Done")

def remove_file(source):
    print("remove file: {}".format(source))
    os.remove(source)

def remove_directory(source):
    print("Remove directory {}".format(source))
    shutil.rmtree(source)

if __name__ == "__main__":

    usage = "usage: %prog [options] drupal_installation_location"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--download",
                        help="Download update from url.",
                        dest="download_url")

    parser.add_option("-i", "--input",
                        help="Path to compressed Drupal package.",
                        dest="local_path")

    (options, args) = parser.parse_args()
    home_directory = path.dirname(path.realpath(__file__))
    

    if len(args) > 0:
        drupal_project_directory = home_directory+"/"+args[0]
    else:
        raise Exception("Error: Drupal project not provided")
    
    print("Args and options", args, options)
    print(dir(options))

    if options.local_path is not None:
        if not path.exists("{}/{}".format(home_directory, options.local_path)):
            raise Exception("Error: Project {} doesn't exist".format(options.local_path))
        else:
            zipped_package_location = "{}/{}".format(home_directory, options.local_path)
            print("Updating from {}".format(zipped_package_location))

    elif options.download_url is not None:
        # Download zipped project
        pass
    else:
        raise Exception("Error: Zipped Drupal project or download URL must be provided")

    if tarfile.is_tarfile(zipped_package_location):
        print("Tarfile")
    elif zipfile.is_zipfile(zipped_package_location):
        print("Zip File")
    else:
        raise Exception("Not a valid update package.")
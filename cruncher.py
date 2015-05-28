import tarfile
import sys
import os
import base64
import zipfile
import argparse


def make_tarfile(output_filename, source_dir):
    output_filename = output_filename + '.tar.gz'
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def make_zipfile(output_filename, source_dir):
    output_filename = output_filename + '.zip'
    relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename): # regular files only
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                    zip.write(filename, arcname)

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-z','--zip',action="store_true",help="Compress directory into a zip file(directories only)")
    group.add_argument("-t","--tar",action="store_true",help="Compress file or directory into a tar file")

    parser.add_argument("fileName", help = "The name of the file you want to compress", type=str)

    args = parser.parse_args()
    outName, ext = args.fileName.split(".")
    if(args.zip):
        if os.path.isdir(args.fileName) == True:
            try:
                make_zipfile(outName, args.fileName)
                print "Compression of " + args.fileName + " into zip file was successful " + args.fileName + ".zip has been created"
            except:
                print "Compression of " + args.fileName + " failed"
        else:
            print "Compression failed can only compress directories into zip files"
    elif(args.tar):
        try:
            make_tarfile(outName, args.fileName)
            print "Compression of " + args.fileName + " into tar file was successful " + args.fileName + ".tar has been created"
        except:
            print "Compression of " + args.fileName + " failed"
            
        


    
if __name__ == '__main__':
    main()

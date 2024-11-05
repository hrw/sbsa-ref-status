#!/usr/bin/python3

import gzip
import hashlib
import lzma
import os
import requests
import shutil
import sys
import yaml

from urllib.parse import urlparse

"""
os.yml file defines list of operating system images to use with boot-sbsa-ref
script. There are several fields defined for each entry:

osname:             used with "--os" argument of boot-sbsa-ref.py script
  checksum:         sha256 checksum
  file:             filename of local copy of disk image (mandatory)
  force-download:   skip checking, always download fresh image
  force-name:       use filename from "file" field (centos8s has boot.iso)
                    otherwise filename from url is used
  paywall_url:      URL to page with image (behind paywall)
  reset:            disable shutdown during run on "boot-sbsa-ref" script
  type:             files are assumed to be ISO, "hdd" tells otherwise
  url:              URL to image

"""


def unpack_file(fin, newname):
    with open(newname, 'wb') as fout:
        shutil.copyfileobj(fin, fout)


def progressbar(filesize, position):
    len = 80
    dots = ""
    for d in range(0, int(len * position / filesize)):
        dots += "."
    for d in range(int(len * position / filesize), len):
        dots += " "
    print(f"\r{dots}\t{position/filesize:.2%}", end='')


def download_os_image(os_name, data):
    if 'url' not in data:
        print(f"Cannot download image for {os_name}.")
        return

    # if image has too generic name (boot.iso in c8s) then
    # we may force our name
    if 'force-name' not in data:
        # if file on disk name != file name in url then use one from url
        if data['url'].split('/')[-1] != data['file'].split('/')[-1]:
            data['file'] = f"disks/{data['url'].split('/')[-1]}"

    print(f"Downloading {os_name} from {data['url']}")

    urlname = f"disks/{os.path.basename(urlparse(data['url']).path)}"
    r = requests.get(data['url'], stream=True)

    try:
        filesize = int(r.headers["Content-Length"]) or None
    except KeyError:
        filesize = None

    checksum = hashlib.sha256()

    if r.status_code != 200:
        print(f"HTTP Error {r.status_code}")
        sys.exit(-1)
    with open(urlname, 'wb') as fd:
        position = 0
        for chunk in r.iter_content(chunk_size=32768):
            fd.write(chunk)
            checksum.update(chunk)
            if filesize:
                position += 32768
                progressbar(filesize, position)

    print(" ")
    print(f"Fetched {urlname}")

    # daily/snapshot images do not have checksums stored
    if data['checksum']:
        if data['checksum'] != checksum.hexdigest():
            print("Checksum does not match")
            print(f"Old one: {data['checksum']}")
            print(f"New one: {checksum.hexdigest()}")

        data['checksum'] = checksum.hexdigest()

    # if file was compressed then unpack it
    if data['url'].endswith('.gz') or data['url'].endswith('.xz'):
        if 'force-name' in data:
            newname = data['file']
        else:
            newname = os.path.splitext(urlname)[0]

        print(f"Unpacking into {newname}")

        if data['url'].endswith('.gz'):
            with gzip.open(urlname, 'rb') as fin:
                unpack_file(fin, newname)
        elif data['url'].endswith('.xz'):
            with lzma.open(data['file'], 'rb') as fin:
                unpack_file(fin, newname)

        os.remove(urlname)
        data['file'] = newname

        print("Done")
    return data


with open("os.yml") as yml:
    yml_data = yaml.safe_load(yml)

wanted_os = ""

if len(sys.argv) > 1:
    wanted_os = sys.argv[1]
    print(f"Updating only image for {wanted_os}")

for entry in yml_data:

    if wanted_os and wanted_os != entry:
        continue

    os_data = yml_data[entry]

    print(f"Checking image for {entry}")

    filename = ""
    if 'file' in os_data:
        filename = os_data['file'].split('/')[-1]
    else:
        os_data['file'] = ""

    if 'url' in os_data:
        url_name = os_data['url'].split('/')[-1]
    else:
        url_name = filename

    try:
        if 'force-download' in os_data:
            print("Force download defined")
            yml_data[entry] = download_os_image(entry, os_data)
        elif filename == url_name:
            # checking do we have file already
            os.stat(os_data['file'])
        elif f"{filename}.gz" == url_name:
            # checking do we have unpacked file already
            os.stat(os_data['file'])
        else:
            # no file, need to download
            yml_data[entry] = download_os_image(entry, os_data)
    except FileNotFoundError:
        yml_data[entry] = download_os_image(entry, os_data)

with open("os.yml", "w") as yml:
    yaml.dump(yml_data, yml)

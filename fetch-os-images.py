#!/usr/bin/python3

import gzip
import os
import requests
import shutil
import sys
import yaml

"""
os.yml file defines list of operating system images to use with boot-sbsa-ref
script. There are several fields defined for each entry:

osname:             used with "--os" argument of boot-sbsa-ref.py script
  file:             filename of local copy of disk image (mandatory)
  force-download:   skip checking, always download fresh image
  force-name:       use filename from "file" field (centos8s has boot.iso)
                    otherwise filename from url is used
  paywall_url:      URL to page with image (behind paywall)
  reset:            disable shutdown during run on "boot-sbsa-ref" script
  type:             files are assumed to be ISO, "hdd" tells otherwise
  url:              URL to image

"""


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

    r = requests.get(data['url'], stream=True)
    with open(data['file'], 'wb') as fd:
        for chunk in r.iter_content(chunk_size=32769):
            fd.write(chunk)

    # if file was gzip compressed then unpack it
    if data['file'].endswith('.gz'):
        newname = os.path.splitext(data['file'])[0]
        with gzip.open(data['file'], 'rb') as fin:
            with open(newname, 'wb') as fout:
                shutil.copyfileobj(fin, fout)
                os.remove(data['file'])
                data['file'] = newname

    return data


with open("os.yml") as yml:
    yml_data = yaml.safe_load(yml)

if len(sys.argv) > 1:
    wanted_os = sys.argv[1]
    print(f"Updating only image for {wanted_os}")

for entry in yml_data:

    if wanted_os and wanted_os != entry:
        continue

    os_data = yml_data[entry]

    print(f"Checking image for {entry}")

    filename = os_data['file'].split('/')[-1]

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

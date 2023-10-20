"""
    GReverse - A tool for OSINT(Open Source Intelligence) gathering & facial recognition via Google Custom Search & Google Vision API's.
    Created by Adrian Tarver(Th3Tr1ckst3r) @ https://github.com/Th3Tr1ckst3r/

////////////////////////////////////////////////////////////////////////////////////////

  IMPORTANT: READ BEFORE DOWNLOADING, COPYING, INSTALLING OR USING.

  By downloading, copying, installing, or using the software you agree to this license.
  If you do not agree to this license, do not download, install,
  copy, or use the software.


                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU Affero General Public License is a free, copyleft license for
software and other kinds of works, specifically designed to ensure
cooperation with the community in the case of network server software.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
our General Public Licenses are intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  Developers that use our General Public Licenses protect your rights
with two steps: (1) assert copyright on the software, and (2) offer
you this License which gives you legal permission to copy, distribute
and/or modify the software.

  A secondary benefit of defending all users' freedom is that
improvements made in alternate versions of the program, if they
receive widespread use, become available for other developers to
incorporate.  Many developers of free software are heartened and
encouraged by the resulting cooperation.  However, in the case of
software used on network servers, this result may fail to come about.
The GNU General Public License permits making a modified version and
letting the public access it on a server without ever releasing its
source code to the public.

  The GNU Affero General Public License is designed specifically to
ensure that, in such cases, the modified source code becomes available
to the community.  It requires the operator of a network server to
provide the source code of the modified version running there to the
users of that server.  Therefore, public use of a modified version, on
a publicly accessible server, gives the public access to the source
code of the modified version.

  An older license, called the Affero General Public License and
published by Affero, was designed to accomplish similar goals.  This is
a different license, not a version of the Affero GPL, but Affero has
released a new version of the Affero GPL which permits relicensing under
this license.

  The precise terms and conditions for copying, distribution and
modification follow here:

https://raw.githubusercontent.com/Th3Tr1ckst3r/GReverse/main/LICENSE

"""
import os
import sys
import re
import json
import requests
import face_recognition
from multiprocessing import Pool, Manager
from tqdm import tqdm
from dict2xml import dict2xml
from urllib.parse import unquote, urlsplit


def downloadImages(image_urls, download_dir, num_procs, facecheck, search_image_path):
    if num_procs > 1:
        manager = Manager()
        file_paths = manager.list()
        parallelDownload(image_urls, download_dir, file_paths, facecheck, search_image_path)
    else:
        file_paths = []
        successful_downloads = 0
        for url in image_urls:
            result = singleDownload(url, download_dir, facecheck, search_image_path)
            if result:
                file_paths.append(result)
                successful_downloads += 1
        print(f"\nSuccessfully downloaded {successful_downloads} out of {len(image_urls)} images.")


def parallelDownload(image_urls, output_folder, file_paths, facecheck, search_image_path):
    args = [(url, output_folder, file_paths, facecheck, search_image_path) for url in image_urls]
    with Pool() as pool:
        for _ in tqdm(pool.imap_unordered(download_and_track_progress, args), total=len(image_urls), desc="Downloading Images"):
            pass

    successful_downloads = len(file_paths)
    print(f"\n\nDownloaded {successful_downloads} out of {len(image_urls)} images successfully.")
    return file_paths


def download_and_track_progress(args):
    url, output_folder, file_paths, facecheck, search_image_path = args
    result = singleDownload(url, output_folder, facecheck, search_image_path)
    if result:
        file_paths.append(result)


def extractUrls(data, searchtype):
    urls = []
    if searchtype == 'image':
        for key in ['pages_with_matching_images', 'full_matching_images', 'visually_similar_images']:
            for item in data.get(key, []):
                if isinstance(item, dict):
                    url = item.get('url')
                    if url:
                        urls.append(url)
                elif isinstance(item, str):
                    urls.append(item)
    elif searchtype == 'query':
        urls = list(data.values())
    return list(set(urls))


def validateUrls(url_list):
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'tif', 'tiff', 'raw', 'bmp', 'psd', 'svg', 'ico']
    valid_urls = []
    for url in url_list:
        extension = urlsplit(url).path.split('.')[-1]
        if extension.lower() in valid_extensions:
            valid_urls.append(url)
    return valid_urls


def formatOutput(results, searchtype, outputtype):
    if outputtype == 'pretty':
        if searchtype == 'image':
            formatted_output = ""
            for key in ['pages_with_matching_images', 'full_matching_images', 'visually_similar_images', 'partial_matching_images']:
                if key in results:
                    formatted_output += f"\n\n{key.capitalize().replace('_', ' ')}:\n\n"
                    for item in results[key]:
                        if isinstance(item, dict) and 'url' in item:
                            formatted_output += f"\n    URL: {item['url']}\n"
                        elif isinstance(item, str):
                            formatted_output += f"\n    URL: {item}\n"
            return formatted_output
        elif searchtype == 'query':
            formatted_output = ""
            for title, url in results.items():
                formatted_output += f"\n    Title:   {title}\n    URL:   {url}\n"
            return formatted_output
    elif outputtype in ['raw', 'json']:
        if searchtype == 'image' and 'json' in results:
            del results['json']
        if outputtype == 'json':
            return json.dumps(results, indent=4, sort_keys=False)
    elif outputtype == 'xml':
        if searchtype == 'image' and 'json' in results:
            del results['json']
        return dict2xml(results, wrap='webDetection', indent="       ")
    else:
        return '\n\nError: Invalid output_type argument.'


def singleDownload(image_url, file_directory, facecheck, search_image_path):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0'}
    if not os.path.isdir(file_directory):
        print(f"\n\nError: Invalid file directory {file_directory}")
        return None
    filename = os.path.basename(unquote(urlsplit(image_url).path))
    file_path = os.path.join(file_directory, filename)
    if os.path.exists(file_path):
        print(f"\n\nFile already exists at {file_path}")
    else:
        try:
            response = requests.get(image_url, headers=header)
            if response.status_code != 200:
                print(f"\n\nError: Failed to download image from {image_url}. Status code: {response.status_code}")
                return None
            with open(file_path, 'wb+') as file:
                file.write(response.content)
            print(f"\n\nDownloaded image from:  {image_url}\n\nSaved as: {filename}")
        except Exception as e:
            print(f"\n\nError: An error occurred while downloading {image_url}: {str(e)}")
            return None
    if facecheck and file_path:
        verify_result = verifyFace(search_image_path, file_path)
        if verify_result:
            print(f"\n\nFacial Match: Image matched for {image_url}")
        else:
            print(f"\n\nFacial Match: Image did not match for {image_url}")
    return file_path


def verifyFace(target_image, test_image):
    try:
        try:
            known_image = face_recognition.load_image_file(known_image_path)
            known_encoding = face_recognition.face_encodings(known_image)[0]
            unknown_image = face_recognition.load_image_file(unknown_image_path)
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        except IndexError:
            return '\n\nError: Face was not detected in {0}'.format(unknown_image_path)
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        return results[0]
    except Exception as e:
        return f"\n\nError: An error occurred during facial recognition: {str(e)}"

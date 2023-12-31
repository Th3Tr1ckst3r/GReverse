<p align="center">
  <img src="https://i.imgur.com/m9cOCGs.png" alt="GReverse Logo" width="300">
</p>

# GReverse

[![License](https://img.shields.io/badge/License-GPL%203.0%20with%20AGPL%203.0-blue.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Th3Tr1ckst3r/GReverse)](https://github.com/Th3Tr1ckst3r/GReverse/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Th3Tr1ckst3r/GReverse)](https://github.com/Th3Tr1ckst3r/GReverse/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/Th3Tr1ckst3r/GReverse)](https://github.com/Th3Tr1ckst3r/GReverse/issues)

A reverse search tool for OSINT (Open Source Intelligence) gathering & facial recognition via Google Custom Search & Google Vision API's.

## About

GReverse is a reverse search tool built for data researchers, penetration testers, security analysts, and more.

## Why Use GReverse?

If all your given is an image, or name and you need more information, with GReverse you are able to perform accurate 
reverse image searches & data searches with a wide range of capabilties using OSINT (Open Source Intelligence).

## Features

- Find full matching images, partial matching images, similar matching images, and more.
- Download results to a local directory of your own choice.
- See data in multiple formats: JSON, XML, RAW(dictionary), and Pretty(Readable Output).
- Utilize the builtin functionality of Python3's multiprocessing library to download images at blazing fast speeds.
- Choose the number of processes you think your system can handle for even faster multiprocessing functionality.
- Run builtin facial recognition against your results to see, if any, are the same person with the [face_recognition](https://pypi.org/project/face-recognition/) library.
- Even restrict your own query searches to do normal Google searches when necessary, all under one hood.

## Screenshots

This is the command line(CLI) interface.

![GReverse_CLI](https://i.imgur.com/2gvqRJs.png)

Demonstration of GReverse with facial recognition enabled.

![Facial_Recognition_Demo](https://i.imgur.com/Ho3Fxan.png)

## Installation Notice

GReverse uses Python3 natively, so you will need to have it installed before proceeding. Once you have done that follow
the steps below.

## Required Libraries Install Guide

To use GReverse, the following Python3 libraries will need to be installed. You can install them using the Python package manager `pip`.
Below are the installation instructions for each library:

1. **Google API Client Library (googleapiclient)**

    You can install the Google API Client Library using `pip`:
    
    ```bash
    pip install google-api-python-client
    ```

2. **Google Cloud Vision (google-cloud-vision)**

    Install the Google Cloud Vision client library using `pip`:
    
    ```bash
    pip install google-cloud-vision
    ```

3. **Protocol Buffers (google.protobuf)**

    You can install the Protocol Buffers library using `pip`:
    
    ```bash
    pip install protobuf
    ```

4. **Face Recognition (face_recognition)**

    Install the Face Recognition library using `pip`:
    
    ```bash
    pip install face_recognition
    ```

5. **TQDM (tqdm)**

    You can install the TQDM library using `pip`:
    
    ```bash
    pip install tqdm
    ```

6. **Dict2XML (dict2xml)**

    Install the Dict2XML library using `pip`:
    
    ```bash
    pip install dict2xml
    ```

With these libraries installed, you can proceed to the next step which is configurations.

## Configurations

To properly configure your Google Python3 installation, follow the guides below:

[Python3_Google_Quickstart_Guide](https://developers.google.com/docs/api/quickstart/python)

Its recommended to have two programmable custom search engines. One configured for images only, and the other for links only.
You will also need to add both search engine ID's to the creds.py file located in the api_creds folder.

[Python3_Custom_Search_Guide](https://developers.google.com/custom-search/docs/overview)

<a name="Contributors"></a>
## Contributors

<p align="center">
    <a href="https://github.com/Th3Tr1ckst3r"><img src="https://avatars.githubusercontent.com/u/21149460?v=4" width=75 height=75></a>
</p>


I welcome you to contribute code to GReverse, and thank you for your contributions, feedback, and support.


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
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.protobuf.json_format import MessageToDict
import requests


def requestData(image_input, max_results=10, titles_to_urls=None):
    client = vision_v1.ImageAnnotatorClient()
    if image_input.startswith('http') or image_input.startswith('https'):
        response = requests.get(image_input)
        image = types.Image(content=response.content)
    else:
        with open(image_input, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
    combined_results = {
        "pages_with_matching_images": [],
        "full_matching_images": [],
        "partial_matching_images": [],
        "visually_similar_images": [],
        "json": None
    }
    num_results = 0
    while num_results < max_results:
        batch_max_results = min(max_results - num_results, 10)
        request = vision_v1.AnnotateImageRequest(
            image=image,
            features=[
                vision_v1.Feature(
                    type_=vision_v1.Feature.Type.WEB_DETECTION,
                    max_results=batch_max_results
                )
            ]
        )
        response = client.annotate_image(request)
        if response.error.message:
            raise Exception(f'Error: {response.error.message}')
        web_detection = response.web_detection
        for page in web_detection.pages_with_matching_images:
            page_title = page.page_title
            url = page.url
            combined_results["pages_with_matching_images"].append({"url": url, "title": page_title})
            num_results += 1
        for full_matching_image in web_detection.full_matching_images:
            full_matching_image_url = full_matching_image.url
            combined_results["full_matching_images"].append(full_matching_image_url)
            num_results += 1
        for partial_matching_image in web_detection.partial_matching_images:
            partial_matching_image_url = partial_matching_image.url
            combined_results["partial_matching_images"].append({"url": partial_matching_image_url})
            num_results += 1
        visually_similar_images = web_detection.visually_similar_images
        combined_results["visually_similar_images"].extend(visually_similar_images)
        if num_results >= max_results:
            combined_results["visually_similar_images"] = combined_results["visually_similar_images"][:max_results]
            break
    json_data = MessageToDict(response._pb)
    if json_data['webDetection']['webEntities']:
        del json_data['webDetection']['webEntities']
    if json_data['webDetection']['bestGuessLabels']:
        del json_data['webDetection']['bestGuessLabels']
    combined_results["json"] = json_data
    return combined_results

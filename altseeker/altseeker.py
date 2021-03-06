#!/usr/bin/env python

"""
Copyright 2016 Parham Pourdavood

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import httplib
import urllib
import ast
import json
import urlparse
import os
import argparse
from bs4 import BeautifulSoup


def is_url(url):
    """
    check to see if the address is a URL or a local path and returns True if
    it is and Fale if it is a local file.

    parameters
    ----------
    url:        str

    returns
    -------
       -        Bool
    """
    return urlparse.urlparse(url).scheme != ""


def caption(image_file, api_key, html_file):
    """
    It takes an image URL and an API key to send a request to
    Microsoft Computer Vision API
    and returns a caption(string) for the image.

    Parameters
    ----------
    image_src:      str
    api_key:        str
                    Microsoft's api_key
    html_file       Abs path to html_file

    Returns
    -------
    captioned_data: str
    """
    if is_url(image_file) is False:
        headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': api_key,
        }
    else:
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': api_key,
        }
    params = urllib.urlencode({
        # Request parameters
        'maxCandidates': '1',
    })

    # Data is the data that takes the image source. It is converted to str
    # using a json method
    if is_url(image_file):
        data = json.dumps({"Url": image_file}, separators=(',', ':'))
    else:
        if os.path.isabs(image_file):
            with open(image_file, 'rb') as f:
                data = f.read()
        else:
            # If the image's path is relative we will find its absolute path
            # by joining it to the html_file's abs path.
            dir_path = os.path.dirname(os.path.realpath(html_file))
            image_file = os.path.join(dir_path, image_file)
            with open(image_file, 'rb') as f:
                data = f.read()
    try:
        conn = httplib.HTTPSConnection('centralindia.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v3.2/describe?%s" %
                     params, data, headers)
        response = conn.getresponse()
        data = ast.literal_eval(response.read())
        # Captioned_data is a JSON that we need to navigate in order to get to
        # the caption text.
        captioned_data = data['description']['captions'][0]["text"]
        return(captioned_data)
        conn.close()
    except Exception:
        print("API call to Microsoft was not successful")


def apply(html_file, api_key):

    """
    It takes an html file and creates a new html file in
    which all the alt attribute of img tags
    are filled out with their related caption. (made by caption
    function in caption module)

    parameters
    ----------
    html_file:		HTML
    api_key:		str
                    Microsoft's api_key
    """

    with open(html_file) as f:
        html_data = f.read()

    # Using a third party library called beautifulSoup for parse and
    # manipulate HTML DOM

    parsed_html = BeautifulSoup(html_data, 'html5lib')

    # Assign all the image tags to img_tages

    img_tags = parsed_html.find_all('img')

    # Goes over each img tag and see if its alt attribute has a value.
    # If it doesn't, it will fill out the alt with the corresponding caption
    # for the image.

    for each_image in img_tags:
        value = each_image.get("alt")

        # It only fills out the image tags that don't have the alt attribute
        if value is None:
            each_image["alt"] = caption(each_image["src"], api_key, html_file)

    res = 0

    # Use this loop to see if a file with the same name exits. If it does, add
    # a suffix.
    while os.path.exists(os.path.dirname(html_file) +
                         "/altseeker" + str(res) + ".html"):
        res += 1

    # Set the output file next to the HTML file
    output_file = open(os.path.dirname(html_file) +
                       "/altseeker" + str(res) + ".html", 'a')
    output_file.write(parsed_html.prettify().encode('utf-8'))
    print("Success! Your new HTML was created at: " +
          os.path.dirname(html_file) + "/altseeker" + str(res) + ".html")


def argParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("html", help="The path to youe html file",
                        type=str)
    parser.add_argument("key", help="Microsoft Cognitive Services Key",
                        type=str)
    args = parser.parse_args()
    try:
        apply(args.html, args.key)
    except ValueError:
        print("Failed to connect to server: Please try again!")


if __name__ == '__main__':
    argParser()

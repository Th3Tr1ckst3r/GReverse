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
import sys
import argparse
from utils.imageSearch import requestData as imageSearch
from utils.querySearch import requestData as querySearch
from utils.dataUtils import *
from api_creds.creds import googleCreds


def main():
    parser = argparse.ArgumentParser(prog='greverse.py',
                                     description="GReverse V1.0 - A reverse search tool for OSINT (Open Source Intelligence) gathering & facial recognition via Google Custom Search & Google Vision API's.", epilog='For more help, please visit:  https://github.com/Th3Tr1ckst3r/GReverse')
    parser.add_argument('--image', type=str, help='Google Vision path to a local image file, or a URL.')
    parser.add_argument('--query', type=str, help='Google Custom Search using a query string.')
    parser.add_argument('--restrict_query', action='store_true', default=False, help='Exclude image output from the query search. In other words, regular Google search for links related to our query.')
    parser.add_argument('--max_results', type=int, default=10, help='Max number of results to return. Default is 10, max is 500 due to API restrictions per request.')
    parser.add_argument('--facecheck', action='store_true', default=False, help='Enable automated, optimized facial recognition across Google Vision results.')
    parser.add_argument('--download_dir', type=str, help='Directory to download images for the purpose of facial recognition.')
    parser.add_argument('--multi', action='store_true', default=False, help='Enable multiprocessing for indexing and downloading images.')
    parser.add_argument('--procs', type=int, default=3, help='Number of processes to use during multiprocessing.')
    parser.add_argument('--output_type', type=str, default='pretty', help='Change the output type for your specific use case. Options include: raw(dict), pretty(formatted), json, and xml.')
    parser.add_argument('--save_output', type=str, default=None, help='Filepath to save output.')
    args = parser.parse_args()
    if args.image:
        results = imageSearch(args.image, args.max_results)
        if args.facecheck and args.download_dir:
            parsed_urls = extractUrls(results, 'image')
            validated_urls = validateUrls(parsed_urls)
            if args.multi:
                downloadImages(validated_urls, args.download_dir, args.procs, args.facecheck, args.image)
            else:
                downloadImages(validated_urls, args.download_dir, 1, args.facecheck, args.image)
        elif args.facecheck:
            print('Error: If you want to run facial recognition, you must specify the --download_dir argument.')
        elif args.download_dir:
            parsed_urls = extractUrls(results, 'image')
            validated_urls = validateUrls(parsed_urls)
            if args.multi:
                downloadImages(validated_urls, args.download_dir, args.procs, False, args.image)
            else:
                downloadImages(validated_urls, args.download_dir, 1, False, args.image)
        else:
            formatted_results = formatOutput(results, 'image', args.output_type)
            if args.save_output is not None and ('/' in args.save_output or '\\' in args.save_output):
                saveOutput(formatted_results, args.output_type, args.save_output)
            else:
                print(formatted_results)
    elif args.query:
        if args.facecheck:
            print('Error: Query search does not support facial recognition, as the search is not being done using an image.')
        elif args.download_dir:
            results = querySearch(args.query, args.max_results, False, googleCreds['devKey'], googleCreds['imageSearchID'])
            parsed_urls = extractUrls(results, 'query')
            if args.multi:
                downloadImages(parsed_urls, args.download_dir, args.procs, False, '')
            else:
                downloadImages(parsed_urls, args.download_dir, 1, False, '')
        elif args.restrict_query:
            results = querySearch(args.query, args.max_results, True, googleCreds['devKey'], googleCreds['querySearchID'])
            formatted_results = formatOutput(results, 'query', args.output_type)
            if args.save_output is not None and ('/' in args.save_output or '\\' in args.save_output):
                saveOutput(formatted_results, args.output_type, args.save_output)
            else:
                print(formatted_results)
        else:
            results = querySearch(args.query, args.max_results, False, googleCreds['devKey'], googleCreds['imageSearchID'])
            formatted_results = formatOutput(results, 'query', args.output_type)
            if args.save_output is not None and ('/' in args.save_output or '\\' in args.save_output):
                saveOutput(formatted_results, args.output_type, args.save_output)
            else:
                print(formatted_results)
    else:
        print('Error: Invalid use of arguments. You must specify either the image argument or query argument.')


if __name__ == "__main__":
    main()
    sys.exit(1)


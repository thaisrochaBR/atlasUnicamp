#!/usr/bin/python3

# -*- coding: utf-8 -*-
__file__
__version__ = '1.0'

import os
from io import BytesIO
import argparse
from datetime import datetime, timedelta, time
from time import sleep, clock
from tqdm import tqdm, trange
from PIL import Image
import requests
import xarray as xr
import netCDF4
import boto3
import matplotlib.pyplot as plt
import PIL
from PIL import Image
class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()  
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)

def confirm(s):
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    print(s)
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("OK to push to continue [Y/n]: ").lower()
        if answer == "":
            answer = "y"
    return answer == "y"

def valid_channel(s):
    try:
        if (int(s) >= 1) and (int(s) <= 16):
            return int(s)
        else:
            msg = "Not a valid channel: '{0}', pick between 1 and 16.".format(s)
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
        msg = "Not a valid channel: '{0}', pick between 1 and 16.".format(s)
        raise argparse.ArgumentTypeError(msg)

def valid_interval(s):
    try:
        if int(s) in [15, 30, 45, 60]:
            return int(s)
        else:
            msg = "Not a valid interval: '{0}', pick between [15, 30, 45, 60].".format(s)
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
        msg = "Not a valid interval: '{0}', pick between [15, 30, 45, 60].".format(s)
        raise argparse.ArgumentTypeError(msg)

def valid_crop(s):
    try:
        msg = str(s)
        raise argparse.ArgumentTypeError(msg)
    except ValueError:
        msg = "Not a valid interval: '{0}', pick between [15, 30, 45, 60].".format(s)
        raise argparse.ArgumentTypeError(msg)

def addMinutes(tm, min):
    fulldate = datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + timedelta(minutes=min)
    return fulldate.time()

def getNameChannel(ch):
    channel = str(ch)
    if len(channel) == 1:
        channel = "0" + channel
    return "ch" + channel

def get_s3_keys(bucket, prefix = ''):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    """
    aws_access_key_id  = ''
    aws_secret_access_key = ''
    print(prefix)
    s3 = boto3.client('s3',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
    kwargs = {'Bucket': bucket}

    if isinstance(prefix, str):
        kwargs['Prefix'] = prefix

    while True:
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            key = obj['Key']
            if key.startswith(prefix):
                yield key
        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break

# define the function blocks
def fifteen():
    return 96

def thirty():
    return 48

def fortyFive():
    return 32

def sexty():
    return 24

def main():
    intervalOptions = {15 : fifteen,
            30 : thirty,
            45 : fortyFive,
            60 : sexty}

    parser = argparse.ArgumentParser(
        description='This is a Unicamp Atlas script by Alison Vilela. (Errors are not yet logged.)',
        prog='unicamp-atlas',
        formatter_class=SmartFormatter)

    parser.add_argument('-v','--version',
        action='version',
        version='%(prog)s ' + __version__),
    parser.add_argument('-y', "--year",
        help="Set year(2019)",
        type=int)
    parser.add_argument('-s', "--startday",
        help="The start day of year format(1)",
        type=int)
    parser.add_argument('-e', "--endday",
        help="The end day of year format(31)",
        type=int)
    parser.add_argument('-c','--channel',
        type=valid_channel,
        default=3,
        help='R|Pick a channel between 1 and 16 (Default: %(default)s)')
    parser.add_argument('-p','--period',
        type=int,
        default=[12],
        help='R|Period in hour of day, please set period in array (Default: %(default)s)')
    parser.add_argument('-o', "--outputpath",
        type=str,
        default=os.getcwd() + '/output',
        help='R|Directory where output needs to be stored (Default: %(default)s)')
    parser.add_argument('-cp','--crop',
        type=int,
        default=[7300,8000,7500,8200],
        nargs='+',
        help='R|Crop the image, please set positions [left, right, top, bottom] (Example: 7300 8000 7500 8200)')

    args = parser.parse_args()

    today = int(datetime.today().strftime('%j'))
    actualYear = datetime.today().year
    
    if not args.year:
        parser.error("argument -y/--year: must have a date set on YEAR")

    if not args.startday:
        parser.error("argument -s/--startday: must have a date set on STARTDAY")

    if args.endday and not args.startday:
        parser.error("argument -e/--endday: must have a date set on STARTDAY")

    if args.startday:
        if not args.endday:
            args.endday = args.startday

        #if args.startday >= today and args.year <= actualYear:
        #    parser.error("argument -s/--startday: can not be equal or after than today(%d)" % today)

        if args.endday < args.startday:
            parser.error("argument -e/--endday: can not be earlier than STARTDAY")

    if len(args.crop) != 4:
        parser.error("argument -cp/--crop: needs 4 values [left, right, top, bottom] (Example: 7300 8000 7500 8200)")

    if confirm("Download will start, do you want to proceed?"):
        print()
        with trange(((args.endday - args.startday)+1) * len(args.period), initial=0, desc='Progress  ', leave=False) as pbTotal:
            while args.startday <= args.endday:
                for hour in args.period:
                    getimage(args.year, args.startday, hour, args.outputpath, args.channel, args.crop)
                    pbTotal.update(1)
                args.startday = args.startday+1
        print()
        #os.remove(outputpath + '/pure')
        print("Done.")

def getimage(year, day, hour, outputpath, channel, crop):
    try:
        bucket_name = 'noaa-goes16'
        product_name = 'ABI-L1b-RadF'
        left = crop[0]
        right = crop[1]
        top = crop[2]
        bottom = crop[3]
        if (int(year)<2019):
            vmc='-M3C'
        elif (int(year)==2019 and int(day)<=119):
            vmc='-M3C'
        else:
            vmc='-M6C'		

        outputpath = outputpath + '/' + getNameChannel(channel) + '/' + str(year).zfill(4) + '/' + str(day).zfill(3) 
        if not os.path.exists(outputpath + '/pure'):
            os.makedirs(outputpath + '/pure')
        keys = get_s3_keys(bucket_name, prefix = product_name+'/'+ 
                            str(year) + '/' + str(day).zfill(3) 
                            + '/' + str(hour).zfill(2) + '/OR_'+
                            product_name + vmc + str(channel).zfill(2))
        key = [key for key in keys][0] # selecting the first measurement taken within the hour		
        link = 'https://' + bucket_name + '.s3.amazonaws.com/' + key
        file_name = key.split('/')[-1].split('.')[0]
        # resp = requests.get(link)
        with open(outputpath + '/pure/' + file_name + '.nc', 'wb') as out_file:
            resp = requests.get(link, stream=True)
            total_length = int(resp.headers.get('content-length'))
            with tqdm(total=total_length, initial=0, desc='Download  ', unit='B', unit_scale=True, leave=False) as pbar:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        out_file.write(chunk)
                        pbar.update(1024)
        with open(outputpath + '/pure/' + file_name + '.nc', 'rb') as in_file:
            nc_bytes = in_file.read()
            nc4_ds = netCDF4.Dataset(file_name, mode='r', memory=nc_bytes)
            store = xr.backends.NetCDF4DataStore(nc4_ds)
            DS = xr.open_dataset(store)
            fig = plt.figure(figsize=(32, 32))
            plt.imshow(DS.Rad[left:right, top:bottom], cmap='gray')
            plt.axis('off')
            plt.savefig(outputpath + '/' + file_name + '_.png', dpi=300, facecolor='w', edgecolor='w', bbox_inches='tight')
            plt.close(fig)
        os.remove(outputpath + '/pure/' + file_name + '.nc')
        image = Image.open(outputpath + '/' + file_name + '_.png')
        new_image = image.resize((255, 255), PIL.Image.ANTIALIAS)
        newfilename=outputpath + '/' + file_name + '.png'
        print(newfilename)
        new_image.save(newfilename)
        image.close()
        os.remove(outputpath + '/' + file_name + '_.png')
        print('image save :'+newfilename)
    except Exception as e:
        print('\n Erro.: ', e)

main()

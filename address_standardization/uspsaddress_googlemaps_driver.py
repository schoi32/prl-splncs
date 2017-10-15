# coding=utf-8
"""
Author: Sou-Cheng Choi
Contributor: Jack Huang
Date: May 27, 2016 -- Aug 3, 2017
Reference: Choi, Sou-Cheng T., Yongheng Lin, and Edward Mulrow. "Comparison of Public-Domain Software and Services for Probabilistic Record Linkage and Address Standardization,” Towards Integrative Machine Learning and Knowledge Extraction, Springer LNAI 10344, 2017. To appear. PDF available at http://tinyurl.com/ydxbjww4

Original instruction:
To standardize address in samplefordatalinkage.csv using Google Maps API on the first two records:

  $ time python uspsaddress_googlemaps_driver.py --n 2 --m 3

To standardize address in samplefordatalinkage.csv with noise:

  $ time python uspsaddress_googlemaps_driver.py --n 2 --m 3 --g 1

To time, use "time" utility on unix and adds up USER + SYS time:

  $ time python uspsaddress_googlemaps_driver.py --n 2 --m 3 --g 1

New instruction:
A typical command (read 2300 records, using method 5, with noise level 0.2, beginning with 4601st record and
ending with 6900th record):
  $ time python uspsaddress_googlemaps_driver.py --n 2300 --m 5 --g 0.2 --t 2300

"""

import argparse
import random
import time

t0 = time.clock()

parser = argparse.ArgumentParser()
parser.add_argument('--n', '--number_of_records', type=int, default=2500, help='number of records', metavar='n')
parser.add_argument('--m', '--method of choice', type=int, default=6, help="""
                            method of choice:
                            1-3: for Google Maps APIs;
                            4: Geocoder.us;
                            5: Data Science Toolkit;
                            6: usaddress.""", metavar='m')
parser.add_argument('--g', '--generate noise', type=float, default=0, help="0.1: to generate noise level 0.1", metavar='g')
parser.add_argument('--t', '--begin line', type=int, default=0, help="6: begin with 7th record", metavar='t')

args = parser.parse_args()
n=args.n
m=args.m
g=args.g
t=args.t

print "n = %s, m = %s, g = %s, t = %s" % (n,m,g,t)

from uspsaddress_googlemaps import uspsaddress_googlemaps

usadd = uspsaddress_googlemaps()
random.seed(0) # for reproducibility
if m>=1 and m<=3:
  usadd.eval_googlemaps(n,m,g,t)
elif m==4:
  usadd.eval_geocoder_us(n,g,t)
elif m==5:
  usadd.eval_data_science_toolkit(n,g,t)
elif m==6:
  usadd.eval_usaddress(n,g,t)

print "\ncpu time = ", time.clock()-t0

#!/usr/bin/env python3

import re, sys, os, subprocess, hashlib, getopt
import urllib.request

def fix_name(name):
    if name == "gperftools-lib":
        return "gperftools-libs"
    if name == "ncurses-lib":
        return "ncurses-libs"
    return name

def get_sha256(url):
    hash = hashlib.sha256()
    remote = urllib.request.urlopen(url)
    hash.update(remote.read())
    return hash.hexdigest()

def update_http_output(o, name, url, sha):
    o.write("http_file(\n")
    o.write('    name = "'+name+'",\n')
    o.write('    sha256 = "'+sha+'",\n')
    o.write('    urls = [\n')
    o.write('        "'+url+'",\n')
    o.write('   ],\n')
    o.write(')\n\n')

inputfile = ''
outputfile = ''

opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["ifile=","ofile="])
for opt, arg in opts:
   if opt == '-h':
      print('test.py -i <inputfile> -o <outputfile>')
      sys.exit()
   elif opt in ("-i", "--ifile"):
      inputfile = arg
   elif opt in ("-o", "--ofile"):
      outputfile = arg

if inputfile == "":
    print('Provide input file: -i <inputfile>')
    sys.exit()

if outputfile == "":
    print('Provide input file: -o <outputfile>')
    sys.exit()

print('Input file is "', inputfile)
print('Output file is "', outputfile)

f = open(inputfile, "r")

deps = re.findall('http_file\(.*?\)', f.read(), re.DOTALL)
if os.path.exists(outputfile):
  os.remove(outputfile)

o = open(outputfile, 'a+')
for d in deps:
    dep = re.split('\n', d)[1]
    name = re.search('\".*?\"',dep, re.DOTALL).group().strip('"')
    fixname = fix_name(name)
    print("Fetch dep:", name)
    result = subprocess.run(["/usr/bin/yumdownloader", "--url", "--urlprotocols", "http", fixname] , stdout=subprocess.PIPE)
    url = re.search('http\:.*?\.rpm', result.stdout.decode("utf-8") , re.DOTALL).group().strip('"')
    sha = get_sha256(url)
    update_http_output(o, name, url, sha) 

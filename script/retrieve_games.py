#!/usr/bin/python3   
#update this with the path to your python

__author__  = "Talfski"
__license__ = "Public Domain"
__version__ = "1.0"


import sys, os, argparse, time,math, re
from subprocess import Popen, PIPE
from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing import Pool
import itertools
from shutil import rmtree

def create_directory(directory):
   try:
      if os.path.exists(directory) and len(directory)>3:
         print (" %s exists already, please delete it first.output file will be done localy." % directory)
      elif(len(directory)>3 ):
         os.mkdir(directory)
   except OSError:  
    print ("Creation of the directory %s failed" % directory)
   else:  
    print ("Successfully created the directory %s " % directory)

    
gid_url="http://www.chessgames.com/perl/chessgame?gid="
chessgames_url = "http://www.chessgames.com/perl/chess.pl?"

def retieve_gamesId(lines_raw):
   games_set=set()
   for line in lines_raw:
      for t in line.find_all('a', href= True) :
         if("/perl/chessgame?gid" in t['href']):
            games_set.add(t['href'].split("=")[-1])
            break
   return ','.join(games_set)


def retrieve_singlegame( gid):
   current_g = gid_url + gid
   try:
      soup = BeautifulSoup(urlopen(current_g),"lxml")
      games_raw = soup.find_all("div", {"id": "olga-data"})
      for game in games_raw:
         return ''.join(str(game['pgn'])+'\n')
   except Exception as excep:
      print(str(excep))

def parse_url(myurl):
   try:
      soup = BeautifulSoup(urlopen(myurl),"lxml")
      lines_raw = soup.find_all("font", {"face":"verdana,arial,helvetica","size":"-1"})
      #Get lines containing the gid 
      return retieve_gamesId(lines_raw)
   except Exception as excep:
      print(str(excep))
      
#Query preparaion 
parser = argparse.ArgumentParser(description="Retrieve all games of a specific player, lines, tournement..")

mandatory_args = parser.add_argument_group( "mandatory argument" )
mandatory_args.add_argument("-o" , "--opening",help="opening code name.Ex {C20+C40+C44} for bishop opening ",type=str,required=True)
parser.add_argument("-m" , "--moves",help="number of moves", default=30,type=int)
parser.add_argument("-mc" , "--movescomp",help="{le or ge} e.g: -mc 30 -c le => not more than 30 moves",default='le',type=str)
parser.add_argument("-y" , "--year",help="year of the game. 1960 by default",type=int,default=1960)
parser.add_argument("-yc" , "--yearcomp",help="le or ge. e.g: -y 1960 -yc le -> Retrieve games before 1960",type=str,default='ge')
parser.add_argument("-r" , "--result",help="{ 1-0 or 0-1 or 1/2-1/2 or nothing}",type=str,default='')
parser.add_argument("-d" , "--debug",help="Activate traces and prints",default=False,type=bool)
parser.add_argument("-out" , "--output_file",help="output text file name ",default='output',type=str)
parser.add_argument("-s" , "--split",help="-s N,split result onto files of N games each",default=1,type=int)
parser.add_argument("-dir" , "--directory",help="Name of directory , e.g : Sicilian",default='.',type=str)
input_args = parser.parse_args()

debug = False
#prepare the url to be curled 
if debug:
    print("Now we will fetch all games satisfying these criteria:")

start = time.time()
for i in vars(input_args):
    if(i !='debug' and i!='output_file' and i !='split' and i !='directory'):
        chessgames_url+=str(i)+'='+str(getattr(input_args, i))+'&'
    else:
        if str(i)=='debug':
            debug = getattr(input_args, i)
        if(str(i)=='output_file' and  getattr(input_args, i) ):
            output_file=getattr(input_args, i)
        if str(i)=='split':
            split = getattr(input_args, i)
        if str(i)=='directory':
            directory = getattr(input_args, i)
            
if debug:
   for i in vars(input_args):
      print(i, getattr(input_args, i))

print('Query to be executed on chessgames.com is :' , chessgames_url)

list_pages=[]
for i in range(50) : 
   myurl = chessgames_url+ "page="+str(i)+'&'
   list_pages.append(myurl)

#search in 10 pages at time
with Pool(25) as p:
   games_gid = p.map(parse_url, list_pages)
   
games_gid = list(filter(None, games_gid)) # trim empty elements
games_gid=[ g.split(',') for g in games_gid] #split each list element onto list of gid
games_gid=list(itertools.chain(*games_gid)) #merge all list of gids
games_gid=list(set(games_gid)) #dirty way to delete annoyong doublon
end1= time.time()

numberofgames=len(games_gid)
print(numberofgames,'game Ids retrieved. The preparation took ',end1-start , 's')

if debug:
    print('games id are:')
    for g in games_gid:
        print(g)

#Now retrievel of games
games_pgn = []
n_jobs= min(math.ceil(numberofgames/5)+1,10) #well let's be polite to not get kicked by chessgames :)

#Fetch N games at the same time, 
with Pool(n_jobs) as p:
   games_pgn = p.map(retrieve_singlegame, games_gid)

if(len(games_pgn) >0):
   print(directory)
   create_directory(directory)
   with open(directory+'/'+output_file+'.txt', 'a+')  as f:
      f.write('\n'.join(games_pgn))
end2 = time.time()

print('Job done! It took in total ',end2-start,'s')

#split 
if split>1 and math.ceil(numberofgames/split) > 1:
   print("let's split output to ",math.ceil(numberofgames/split),'output file.')
   #TODO

__author__  = "Talfski"
__license__ = "Public Domain"
__version__ = "1.0"


import sys, argparse, re, time
from subprocess import Popen, PIPE
from bs4 import BeautifulSoup
from urllib.request import urlopen

gid_url="http://www.chessgames.com/perl/chessgame?gid="

def retrieve_singlegame( gid, f):
   current_g = gid_url + gid
   soup = BeautifulSoup(urlopen(current_g),"lxml")
   games_raw = soup.find_all("div", {"id": "olga-data"})
   for game in games_raw:
      print(game['pgn'], file=f)
      print('\n', file=f)
   
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
parser.add_argument("-out" , "--output_file",help="output text file ",default='output.txt',type=str)
parser.add_argument("-s" , "--split",help="-s N,split result onto files of N games each",default=1,type=int)

input_args = parser.parse_args()

url = "http://www.chessgames.com/perl/chess.pl?"
debug = False
#prepare the url to be curled 
if debug:
    print("Now we will fetch all games satisfying these criteria:")

start = time.time()
for i in vars(input_args):
    if(i !='debug' and i!='output_file'):
        url+=str(i)+'='+str(getattr(input_args, i))+'&'
    else:
        if str(i)=='debug':
            debug = getattr(input_args, i)
        if(str(i)=='output_file' and  getattr(input_args, i) ):
            output_file=getattr(input_args, i)
    if debug:
        print(i, getattr(input_args, i))

print('Query to be executed on chessgames.com is :' , url)

games_set=set()
numberofpages= 1
for i in range(50) : 
    myurl = url+ "page="+str(i)+'&'
    soup = BeautifulSoup(urlopen(myurl),"lxml")
    found =False
    lines_raw = soup.find_all("font", {"face":"verdana,arial,helvetica","size":"-1"})
    #Get lines containing the gid 
    for line in lines_raw:
        for t in line.find_all('a', href= True) :
            if("/perl/chessgame?gid" in t['href']):
                games_set.add(t['href'].split("=")[-1])
                found=True
                break
    if not found :
        numberofpages=i-1
        break;

end1= time.time()
numberofgames = len(games_set) 
print(numberofgames , ' games are retrieved. It took ',end1-start,'s. Script stopped at page ',numberofpages)

if debug:
    print('games id are:')
    for g in games_set:
        print(g)

#Now retrievel of games
with open(output_file, 'w') as f:
    for gid in games_set:
       retrieve_singlegame( gid, f)
       
end2 = time.time()

print('Job done! It took in total ',end2-start,'s')

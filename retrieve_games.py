__author__  = "Talfski"
__license__ = "Public Domain"
__version__ = "1.0"


import sys, argparse, re
from subprocess import Popen, PIPE
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen

# Query preparaion 
parser = argparse.ArgumentParser(description="Retrieve all games of a specific player, lines, tournement..")
parser = argparse.ArgumentParser(description="Example of use : ")

mandatory_args = parser.add_argument_group( "mandatory argument" )
mandatory_args.add_argument("-o" , "--opening",help="opening code name.Ex {C20+C40+C44} for bishop opening ",type=str,required=True)
mandatory_args.add_argument("-m" , "--moves",help="number of moves", default=30,type=int)
mandatory_args.add_argument("-mc" , "--movescomp",help="{le or ge} e.g: -mc 30 -c le => not more than 30 moves",default='le',type=str)
parser.add_argument("-y" , "--year",help="year of the game. 1960 by default",type=int,default=1960)
parser.add_argument("-yc" , "--yearcomp",help="le or ge. e.g: -y 1960 -yc le -> Retrieve games before 1960",type=str,default='ge')
parser.add_argument("-r" , "--result",help="{ 1-0 or 0-1 or 1/2-1/2 or nothing}",type=str,default='')
parser.add_argument("-d" , "--debug",help="Activate traces and prints",default=False,type=bool)
parser.add_argument("-out" , "--output_file",help="output text file ",default='output.txt',type=str)


input_args = parser.parse_args()

url = "http://www.chessgames.com/perl/chess.pl?"
debug = False
#prepare the url to be curled 
if debug:
    print("Now we will fetch all games satisfying these criteria:")

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

# Curling ...
my_games=[]
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

# Max pages returned by chessgames is 50 so let's loop until 50 
for i in range(50): 
    myurl = url+ "page="+str(i)+'&'
    get = Popen(['curl', '-s', '-A', user_agent, myurl], stdout=PIPE)
    result = get.stdout.read().decode('utf8').split('\n')
    # Get lines containing the gid 
    for i in result:
        if "/perl/chessgame?gid=" in i:
            # grep on the gid and get the whole integer after this str
            s = re.findall('\gid=.[0-9]+',i)
            my_games.append(s[0].split("=")[1])

            if debug:
                print(s[0])

print(len(my_games) , ' games are retrieved.')

if debug:
    print('games id are:')
    for g in my_games:
        print(g)

#Now retrievel of games
gid_url="http://www.chessgames.com/perl/chessgame?gid="
pageid=1

with open(output_file, 'w') as f:
    for gid in my_games:
        current_g = gid_url + gid
        soup = BeautifulSoup(urlopen(current_g),"lxml")
        games_raw = soup.find_all("div", {"id": "olga-data"})
        for game in games_raw:
            print(game['pgn'], file=f)
            print('\n', file=f)
        


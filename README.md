# ChessTools
Some chess tools

# How to use 
For the moment it is launched via command lines try this to see the help manual
    python3 retrieve_games.py -h

# Examples

    command : python3 retrieve_games.py
    usage: retrieve_games.py [-h] -o OPENING [-m MOVES] [-mc MOVESCOMP] [-y YEAR]
                         [-yc YEARCOMP] [-r RESULT] [-d DEBUG]
                         [-out OUTPUT_FILE]
There are some mandatory arguments to avoid rejecting the query by chessgames website such as 
    - opening, ECO codes are used to filter on this

Optional parameters have some default values 
    - year of the game is by default 1960
    - yc (year comparison) to filter games after a specific date or before or exactly by default it is greater or equal (ge).
    - m (moves) number of moves by default is 30
    - mc (moves comparison) less or greater or exactly. By default it is ge
    - r (result) 1-0, 0-1 ,1/2-1/2. if nothing is given it will retrieve the games with various results.
    - d (debug) for debugging by default it is deactivated unless you put -d "something"
    - out to provide an output file. BY default it will create a local file with name output.txt

The output.txt file has been generated by this command
    - python3 retrieve_games.py -o C27 -r 1-0 -y 2018

You can also retrieve many opening lines in the same query ( check manyopening.txt file)
     - python3 retrieve_games.py -o C27+A30+D27 -r 1-0 -y 2018 -out manyopening.txt
     - Query to be executed on chessgames.com is : http://www.chessgames.com/perl/chess.pl?yearcomp=ge&opening=C27+A30+D27&result=1-0&moves=30&year=2018&movescomp=le&
     - 20  games are retrieved.
     
# Some usefull application
    - You can use directly the output file to generate studies on lichess.com website ( see screenshots)
    - To be used to generate look alike style in some specific lines and play against it.

# Ideas:
    - Lichess allow only 20 games per import, so there will be also a feature to split the output file onto many small text files of N games each




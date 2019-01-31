-------------------------------------------------
***Dependencies***
-------------------------------------------------
python3

Python packages

py2p
time
datetime
pandas
numpy

-------------------------------------------------
***DEMO***
-------------------------------------------------

to execute locally:
1) from /localdemo run peerNode.py (it will reference /localdemo/config and strs)
2) run peerNode.py where it is (it will reference config.txt and strs.txt)
3) 2nd instance should query first (and all connected). Result should be 1/1 yes for two node network using these config and str files

-------------------------------------------------
***Y-STR Query Syntax
-------------------------------------------------

1) OPERATOR QUERY

Query can contain unlimited AND clauses containing "=", "<", or ">" logical operators

$STR_NAME1<$VALUE1 and $STR_NAME2=$VALUE2 and ...

2) GENETIC DISTANCE QUERY

Can query to find those with genetic distance less than or equal to a cutoff

GD($STR_NAME1=$VALUE1,$STR_NAME2=$VALUE2, ...)<=$CUTOFF

example: GD(Y-GATA-H4=10,DYS445=6,DYS444=11,DYS464=12-15-15-17)<=3

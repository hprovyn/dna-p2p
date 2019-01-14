-------------------------------------------------
***Dependencies***
-------------------------------------------------
python3

Python packages

py2p
time
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

Query can contain unlimited AND clauses containing "=", "<", or ">" logical operators

$STR_NAME1<$VALUE1 and $STR_NAME2=$VALUE2 and ...
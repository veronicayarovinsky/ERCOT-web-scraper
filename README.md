# ERCOT-web-scraper

The ERCOT-web-scraper is a program that downloads LMPs by Resource Nodes, Load Zones and Trading Hubs from the [ERCOT website](https://www.ercot.com/mktinfo/prices).
* The data is stored as csv files named exactly as on the ERCOT website (without the .zip)
* If files downloaded by this program exist in the given pathname, the program only downloads the new data files (no repeat files).


### How to run it:
Edit the desired pathname (`PATH_NAME`) in the code, then from terminal run either the command `python3 scraper.py` or `python scraper.py` depending on the installed python version.


### Limitations:
* No file organization
* Path for the folder to save data must be edited in the code
* No way to deal with server crashes or nonexistent pathnames

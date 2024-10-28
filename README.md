# IOI-data
 
Repository to collect IOI(International Olympiad in Informatics) data.
And perform data analysis on it.

All data is stored in the `data` directory, and it was scraped from the official IOI-stats website(https://stats.ioinformatics.org/).

To use the package, you can install all dependencies by running `pip install -r requirements.txt` in an environment with Python 3.11.

So far, the only implemented methods are to get the data from the website and to save it to different csv files in the `data` directory.

If you download the whole repository, you don't need to run the scraping script, as the data is already there.

In case you don't have the `data` directory, you can run the `scrape_all_data.py` script in the root directory to get all the data from the website.

Soon methods for queries and plots will be implemented.
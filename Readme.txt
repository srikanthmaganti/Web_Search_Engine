# @author Srikanth Maganti
# UID : 665398395
# Net Id : smagan20
# University of Illinois, Chicago
# CS 582, Spring 2020
# Final Project - A Web Search Engine

Instructions for executing the program:

Required packages :
1. sys
2. pathlib
4. os
5. requests
6. urljoin
7. BeautifulSoup
9. string
10. nltk
11. math
12. collections
13. easygui

Execution steps:

1. As all the pickle files are stored in the current directory which are shared with you so there is no need to run web_crawler.py, and Preprocessing.py.

2. So to check the software just run main_file.py with all the pickle files downloaded in the local directory where python file is downloaded. 

3. Before executing main_file.py go to the location in cmd where main_file.py python file is residing and then execute the program

Note: please make sure to download all the necessary packages

Execution from scratch -

Functionality: 

1. The logic is written in three python files web_crawler.py, main_file.py, and Preprocessing.py


2. web_crawler.py does the crawling of the web pages.First you need to create empty folder named Crawled_data in the local directory. 

3. After all the extracted data got stored in that directory, 2 new pickle files will be created "url_dict.pickle" and "outlinks.pickle". Ignore outlinks.pickle file

4. Now execute Preprocessing.py, after executing this file you can see 2 new pickle files they are docnum_tokens.pickle and tf.pickle

Note: before executing this file set the path for document extraction to your local directory where Crawled_data is located 

5. After checking for all the pickle files. you can start executing main_file.py

6. Once you are done with this execution you will be popping up with 
Graphical user interface to search query.

7.From that step onwards it is easily understandable and you can finally check for the results
 











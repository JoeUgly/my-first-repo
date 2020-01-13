# Joe's Jorbs
## Search for jobs in New York State.

Version: 1.0\
Date: 4/19<br><br>


**This program has a list of all known employment webpages in New York State for:**

- NYS Civil Service municipalities
- Public school districts and charter schools
- Colleges and Universities<br><br>


## Prerequisites:
Python 3.6 or later. Available at: https://www.python.org/downloads/

Copy and Paste the code into a text file and save it with a .py extension. Example:\
jj.py

Executable files available upon request.<br><br>


## Features:

- Searches for any of the user-specified job titles on each page.
- Multiprocessing.
- Limit the search to a geographic distance.
- Smart crawling will only navigate to websites that are likely to contain job postings, based on the contents of the link.
- Skip duplicate webpages.
- Omit duplicate results.
- Omit hidden HTML elements (beta)
- Sort results by how likely they are to contain job postings.
- Limit number of results from each domain.
- Option to open results in browser
- Basic GUI (deprecated)<br><br>


## Input Tips:

Any user input is case-insensitive.

The user-specified job titles are called keywords.

For a job posting to match successfully it must contain the entire exact keyword. For example:\
A job posting for a "Water Plant Operator" would NOT match the keyword "wastewater plant operator", because it doesn't include "wastewater".\
However, it would match the keyword "plant operator".

This program can not find results if they are similar or synonyms to your keyword. For example:\
A job posting for a "Correctional Officer" would NOT match the keyword "corrections officer", because of the difference in spelling.\
In this case you should input all synonyms. E.g. correctional officer, corrections officer, prison guard, etc.

Using a less specific keyword will help get more results. For example:\
A job posting for a "Correctional Officer" would match the keyword "correction". You don't want to be too vague because it will yield false positives.<br><br>


## External Resources:

This program excludes results from centralized job posting websites. I suggest you browse these sites manually.\
Excluded sites:\
OLAS at https://www.pnwboces.org/olas/#!/jobs  
https://monroe2boces.recruitfront.com/JobBoard<br><br>


## Advanced Options Page:

**All links** = Invoke this option to disable jobwords and bunkwords. This will search all links found on each webpage, not just the links most likely to contain job postings, therefore it will take much longer to search and yield more results.\
    Default = disabled

**Write to file** = Invoke this option to write the search results and an error log as text files. It will create a directory called "Jorbs" in the user's home directory and save them there.\
    Default = disabled

**Verbose** = Invoke this option to print lots of extra info to the console. Use for debugging.\
You will need to change the GUI filename extension from ".pyw" to ".py" to see the console.\
    Default = disabled

**Number of processes** = The number you enter here will determine how fast your search is performed. A higher number will take less time, but will use more of your computer's resources.\
I would not use a number much greater than 40 due to diminishing returns and the possibility of crashing.\
    Default = 32

**Max crawl depth** = The number you enter here will determine how thorough of a search to perform. A higher number should find more results, but will take more time and yield less reliable results.\
I would not use a number greater than 3 due to diminishing returns and the exponential increase in number of pages searched.\
    Default = 2

















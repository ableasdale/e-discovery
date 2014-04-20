# e-discovery #

Using the freely available [Enron Email Dataset](http://www.cs.cmu.edu/~./enron/ "View information on the Enron Email Dataset"), this project contains a method for converting the original emails into slightly more structured content (sufficient for loading into MarkLogic and configuring some basic range indexes to build a basic search application).

## Getting started ##

You will need the following:

- [Python 3](https://www.python.org/downloads/ "Get Python from here")
- [MarkLogic Server](http://developer.marklogic.com/products "Download MarkLogic here")
- The [Enron Email Dataset](http://www.cs.cmu.edu/~./enron/enron_mail_20110402.tgz "Download the .tgz file here (~423GB)") 

## Setup ##

Install and configure MarkLogic Server, using [Query Console](http://localhost:8000/qconsole/), ensure the **App-Services** content source is selected and copy / paste the contents of **src/main/xquery/setup.xqy** into the query buffer.  This should configure the following:

- **enron** Database and Forest
- String and DateTime range indexes
- A ReST Application Server listening on port 8003

## Loading the Enron Email Dataset ##

The python script in **src/main/python/prepare-data.py** will traverse the folder structure from the top-down, create XML metadata around each of the emails (From, To, Subject, DateTime) and will use the ReST Application server to load each of the emails into MarkLogic (you will need to configure the **username** / **password** for the application server and ensure the path to the *untarred* enron email set is correct. 
# mini Time.mk
A news aggregation site

### Summary
The aim of the application is to collect and process news articles from different sources with given categories, perform Hierarchical Agglomerative Clustering on the news articles, find the most relevant category for each of the clusters and rank them depending on the different sources in the cluster and the posting time of the articles.
The application uses a MySQL database for storing the data and the Web2py framework for working with the database, handling requests and scheduling the update function.

### Credits
The application was developed by:
* [Robert Armenski](https://github.com/T1T4N)
* [Martin Boncanoski](https://github.com/makedon4e)
* [Goce Cvetanov](https://github.com/cvetanov)
* [Daniel Stojkov](https://github.com/DanielStojkov)

Under the mentorship of:
* [Dr. Igor Trajkovski](http://www.time.mk/trajkovski)
* [Dr. Katerina Zdravkova](http://www.finki.ukim.mk/en/staff/katerina-zdravkova)

### Benchmark
The application is optimized for performance and these are the measured times:
* 3050 posts processed in 19125 ms
* Posts inserted in db in 22460 ms
* tf-idf finished in 1135 ms
* HAC finished in 1076 ms
* Generating static pages: 3562 ms

### Setup instructions:
1. Install Python v2.7.* 32-bit
2. Install the following Python packages:
    * pyquery
    * speedparser
    * pywin32 (if you are using Windows)
    * urllib3
    * lxml
    * libxml2-python (if you are using Windows)

3. Install an Apache server with MySQL
4. Create a database called "timemk" and import the timemk.sql file
5. In the web2py\applications\MiniTimeMK\models\db.py file edit the 15th line with your MySQL credentials
    * If the username is root and the password is blank, no need to edit

6. Enter the web2py directory and to start the webserver, run the following command:
    * python web2py.py -a admin_password -p 8001 -D 30 -K MiniTimeMK -X

7. For a manual site update visit the link 127.0.0.1:8001/update
8. To configure the automatic update task, go to the following link: http://127.0.0.1:8001/MiniTimeMK/appadmin/insert/db/scheduler_task
    * For function name, select "update_task"
    * For period, enter 600 (or any other time interval in seconds)
    * For timeout, enter 240 (or any other time interval in seconds)
    * Click submit

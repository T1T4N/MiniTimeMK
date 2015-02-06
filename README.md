# mini Time.mk
A news aggregator and classifier system

### Setup instructions:
1. Install Python v2.7.*
2. Install the following Python packages:
    * pyquery
    * speedparser
    * pywin32 (if you are using Windows)
    * urllib	
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
    * For period, enter 600
    * For timeout, enter 240
    * Click submit
# TV-Series-Reminder

A python script where it takes your 'email-id' and a list of your favorite 'TV shows' as input and e-mails you a report on the status of the TV shows you entered. Multiple users can use it at once.

## Approach

The whole script has been written in Python3 where the it simply scrapes the data of TV series from the IMDb website (http://imdb.com) and accordingly makes a report to be mailed to the user. 

## Prerequisites

You need to make sure that every library used in the code must be already installed or you can install it using pip install or sudo-apt install as per your OS requirements. 

## Variable Notes

1. Please change the "root" & "pass" (line 13) as per your MySQL username & password. (conn=MySQLdb.connect("localhost","root","pass") )
2. Please change the sender's email id as per your requirement (line 225). (send_mail = "example@gmail.com")
3. Please change the sender's email id password as per your requirement (line 226). (your_pass = "password")
4. Please make sure that your "Allow low secure apps" on your email turned on while you're using the script.

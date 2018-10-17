import urllib.request, urllib.parse, urllib.error, datetime
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import string
import re
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

conn = MySQLdb.connect("localhost","root","pass")
crs = conn.cursor()

def db():
    crs.execute("Create database if not exists innov")
    crs.execute("Use innov")
    create_table = """CREATE TABLE if not exists tvshow_users (email_id varchar(100),tv_shows varchar(600))"""
    crs.execute(create_table)

def test_email(email):  #Function for validating email-ids.
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    if not re.match(pattern, email):
        return -1
    else:
        return 1

def set_date(air_date):  #Function for setting date.
    months = ['Jan','Feb','Mar','May','Apr','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    temp = air_date
    date1 = int(air_date[0:2])
    month1 = temp[3:6]
    month2 = 0
    for i in range(len(months)):
        if month1==months[i]:
            month2 = i + 1
    year1 = int(air_date[-4:])
    date2 = "%i-%i-%i"%(year1, month2, date1)
    return date2
    
def comp_date(d1, current):  #Function for comparing dates.
    date1 = d1.split("-")
    date2 = current.split("-")
    for i in range(3):
        if int(date1[i])>int(date2[i]):
            return d1
        elif int(date1[i])==int(date2[i]):
            continue
        elif int(date1[i])<int(date2[i]):
            return current


def db_f(e_mail, t_v):  #Function for storing the data in the database.
    db()
    query_ = """INSERT INTO tvshow_users (email_id,tv_shows) VALUES (%s,%s)"""
    crs.execute(query_, (e_mail, t_v))
    conn.commit()



users = int(input('Please enter the number of users - \n'))  #For multiple users at once.
email = []  #A list for all the e-mails.
tv_series = []  #A list containing list of tv series for each user.

for user_ in range(users):  #Taking input from users
    p = -1
    while p==-1:
        temp_mail = input('Please enter your e-mail ID - \nEmail address: ')  
        p = test_email(temp_mail) 
        if p==-1:
            print("Wrong format, please enter your e-mail ID again - \n")
        else:
            email.append(temp_mail)
    
    b = ""
    while b=="":
        temp_tv = input('Please enter your desired TV series- \nTV Series: ')
        if temp_tv=="":
            print("Wrong format, please enter again.\n")
        else:
            b = 'a'
    tv_series.append(temp_tv)
    
    

if users > 1:  #Simple pre-confirmation that the process is starting now.
    print("You all would be receiving a email alert shortly!\n")
else:
    print("You will be receiving a email alert shortly!\n")

    
for tv_ser, email_f in zip(tv_series, email):
    tvseries = tv_ser.split(',')    
    
    tv_list = []
    final_list = []
    link_list = []
    flag = []
    for series in tvseries:
        flag.append(1)
        
    num = 0
    
    for series in tvseries:
        temp = series.strip()  #Stripping Tv Series Name from the input list.
        series2 = temp.split(" ")  #Tokenizing the series title.   

        query="+".join(str(i) for i in series2)  #Constructing the search query.

        imdb = 'https://www.imdb.com'

        url = "https://www.imdb.com/find?q=" + query + "&s=tt&ttype=tv&ref_=fn_tv"  #Constructing imdb search url.
        html = urllib.request.urlopen(url).read()  
        soup = BeautifulSoup(html, 'html.parser')  #Creating BeautifulSoup structure to parse webpage.
        
        if soup.find_all(class_ = "article")[0].h1.text.strip()=="No results found for " + '"' + temp + '"':
            flag[num] = 0
            result = "<p>There is no such TV Series titled " + temp + ".</p><br />"
            
        else:     
            name = soup.find_all(class_ = "result_text")[0].a.get('href')  #Storing the first result. 
            url2 = imdb + name  #Constructing imdb tv series url.
            link_list.append(url2)


            html1 = urllib.request.urlopen(url2).read()
            soup1 = BeautifulSoup(html1, 'html.parser')  #Creating BeautifulSoup structure to parse webpage.


            c_title = soup1.find_all(class_ = "title_wrapper")[0].h1.text.strip()
            tv_list.append(c_title)


            name1 = soup1.find_all(class_ = "seasons-and-year-nav")[0].a.get('href')  #Storing the latest season.
            url3 = imdb + name1  #Constructing latest season url.
            

            html2 = urllib.request.urlopen(url3).read()
            soup2 = BeautifulSoup(html2, 'html.parser')  #Creating BeautifulSoup structure to parse webpage.
            name2 = soup2.find_all(class_ = "airdate")  #Storing airdates of the latest season.


            temp_list=[]  #Episode List


            for r in name2:
                temp_list.append(r.get_text().strip())  #Stroring in Episode List


            ep_list = []
            for x in temp_list:
                if not len(x)<4:
                    ep_list.append(x)


            yr = ep_list[0][-4:]


            count = 0


            for r in range(len(ep_list)):
                new_yr = ep_list[r][-4:]


                if len(ep_list[r])>4:
                    temp_date = set_date(ep_list[r])

                    today = datetime.date.today().strftime('%Y-%m-%d')

                    result_date = comp_date(temp_date, today)

                    if result_date==temp_date:
                        result = "The next episode airs on " + (temp_date) + "."
                        break

                    elif result_date==today:
                        count = count+1

                    if count==len(ep_list):
                        result = "The show has finished streaming all its episodes."
                        break

                elif len(ep_list[r])==4:
                    if int(yr) > datetime.datetime.today().year:
                        result = "The next season begins in " + yr + "."
                        break

                    elif int(new_yr) < datetime.datetime.today().year:
                        count = count + 1

                    elif int(new_yr) > datetime.datetime.today().year:
                        result = "The next episode airs on " + new_yr + "...."
                        break

                    if count==len(ep_list):
                        result = "The show has finished streaming all its episodes."

        final_list.append(result)
        num = num + 1


    result = ""
    temp_f = []
    #For MIMEText(result,'html')
    for i, j in zip(final_list, flag):
        if j == 0:
            result = result + i
        else:
            temp_f.append(i)
    
    tv_l = ""
    for i, j, k, m in zip(tv_list, temp_f, link_list, flag):
        result = result + "<p>Tv series name: " + '<a href="' + k + '">' + i + "</a></p>" + "<p>Status: " + j + "</p><br />"
        tv_l = tv_l + i + ", "
    
    tv_l = tv_l[:-2]
    db_f(email_f, tv_l)
    
    #For MIMEText(result, 'plain')
    #for i, j, k in zip(tv_list, final_list, link_list):
    #   result = result + "Tv series name: " + i + "\nStatus: " + j + "\n\n"

    send_mail = "example@gmail.com" 
    your_pass = "password"
    msg = MIMEMultipart()
    msg['From'] = send_mail
    msg['To'] = email_f
    msg['Subject'] = "[Alert] Your Favorite TV Series Episode Reminder"
    TO = email_f
    FROM = send_mail
    msg.attach(MIMEText(result,'html'))

    server = smtplib.SMTP('smtp.gmail.com')

    server.starttls()

    server.login(send_mail, your_pass)
    server.sendmail(FROM, [TO], msg.as_string())
    server.quit()

conn.close()
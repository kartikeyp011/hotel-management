import mysql.connector

mydb = mysql.connector.connect(host='localhost',user='root',password='mysql@1234',database='hotel_management')

mycursor = mydb.cursor(buffered = True)

SecQues = ['What is the name of your first pet?','Which elementary school did you attend?','What is the name of the town where you were born?','What is your favourite movie?','What is your favourite song?']

def start():
    print("                                                                                 WELCOME TO TAJ HOTEL")
    n = int(input("1.Login \n2.Sign Up \nEnter: "))
    if n == 1:
        Login()
    elif n == 2:
        Signup()
    else:
        print("Incorrect Input. Please Try Again.")
        Customer()

def Login():
    print("")
    mycursor.execute("SELECT Email_ID FROM non_subs")
    myresult1 = mycursor.fetchall()
    mycursor.execute("SELECT Email_ID FROM subs_users")
    myresult2 = mycursor.fetchall()
    mail = input("Please Enter Your Mail Id: ")

    if (mail,) in myresult1:
        while True:
            pw = input("Please Enter The Password: ")
            sql = "SELECT Password FROM non_subs WHERE Email_ID = (%s)"
            val = (mail,)
            mycursor.execute(sql,val)
            myresult = mycursor.fetchone()
            if (pw,) == myresult:
                NonSub_User_Dashboard(mail,pw)
            else:
                n = int(input("Wrong Password. \nEnter (1)- To Try Again\nOr (2)- Change mail ID\n3.Forgot Password\nEnter: "))
                if n==2:
                    Login()
                elif n==3:
                    Rec_Pw(mail,"")

    elif (mail,) in myresult2:
        while True:
            pw = input("Please Enter The Password: ")
            sql = "SELECT Password FROM subs_users WHERE Email_ID = (%s)"
            val = (mail,)
            mycursor.execute(sql,val)
            myresult = mycursor.fetchone()
            if (pw,) == myresult:
                Sub_User_Dashboard(mail,pw)
            else:
                n = int(input("Wrong Password. \nEnter (1)- To Try Again\nOr (2)- Change mail ID\n3.Forgot Password\nEnter: "))
                if n==2:
                    Login()
                elif n==3:
                    Rec_Pw(mail,"sub")

def Signup():
    print("")
    mycursor.execute("SELECT Email_ID FROM non_subs")
    myresult1 = mycursor.fetchall()
    mycursor.execute("SELECT Email_ID FROM subs_users")
    myresult2 = mycursor.fetchall()
    mail = input("Enter Your Mail Id: ")
    if (mail,) not in myresult1:
        if (mail,) not in myresult2:
            Name = input("Enter Your Name: ")
            pw = input("Create a Password: ")
            mycursor.execute("SELECT MAX(Cust_ID) FROM non_subs")
            myresult4 = mycursor.fetchone()
            sql = "INSERT INTO non_subs (Cust_ID, Name, Email_ID, Password) VALUES(%s,%s,%s,%s)"
            val = (myresult4[0]+1, Name, mail, pw)
            mycursor.execute(sql,val)
            mydb.commit()
            NonSub_User_Dashboard(pw,mail)
        else:
            print("Error. You already have an Account. Please login there.\nRedirecting to Login Page")
            Login()
    else:
        print("Error. You already have an Account. Please login there.\nRedirecting to Login Page")
        Login()

def Sub_User_Dashboard(mail,pw):
    print("")
    n = int(input("1. See Current Bookings \n2.Book A Room \n3.Change Account Info \n4.Logout \nEnter your choice: "))
    if n==1:
        Cur_Book(mail,pw,"sub")
    elif n==2:
        NewRoom(mail,pw,"sub")
    elif n==3:
        Change_Info(mail,pw,"sub")
    elif n==4:
        Logout()
    else:
        print("Incorrect Input. Pls Enter Again")
        User_Dashboard(mail,pw)

def NonSub_User_Dashboard(mail,pw):
    print("")
    n = int(input("1. See Current Bookings \n2.Book A Room \n3.Change Account Info \n4.Logout \nEnter your choice: "))
    if n==1:
        Cur_Book(mail,pw,"")
    elif n==2:
        NewRoom(mail,pw,"")
    elif n==3:
        Change_Info(mail,pw,"")
    elif n==4:
        Logout()
    else:
        print("Incorrect Input. Pls Enter Again")
        User_Dashboard(mail,pw)

def Cur_Book(mail,pw,s):
    print("")
    if s == "sub":
        mycursor.execute("SELECT Cur_Bookings FROM subs_users")
        myresult = mycursor.fetchall()
        print("Your Current Bookings: ")
        for x in myresult:
            if myresult != (None,):
                print("    ",end = x)
            else:
                print("No Current Bookings.")
        Sub_User_Dashboard(mail,pw)
    else:
        mycursor.execute("SELECT Cur_Bookings FROM non_subs")
        myresult = mycursor.fetchone()
        print("Your Current Bookings: ")
        for x in myresult:
            if myresult != (None,):
                print("    ",end = x)
            else:
                print("No Current Bookings.")
        NonSub_User_Dashboard(mail,pw)

def NewRoom(mail,pw,s):
    print("")
    if s == "sub":
        dt = input("Pls Enter Date when you want to stay (Format: YYYY-MM-DD): ")
        sql = "SELECT Room_No, Room_Type, Price_per_Night, Features FROM rooms WHERE Booked_Till < \""+dt+"\""
        mycursor.execute(sql)
        mydb.commit()
        myresult = mycursor.fetchall()
        print("Available Rooms ")
        for x in myresult:
            print("Room",x[0],": ",x[1])
            print("      Features: ",x[3])
            print("      Price per night: ",x[2])
        print("")
        while True:
            n = input("Pls Enter the Room_No of the Room which you would like to book: ")
            for i in range(0,len(myresult)):
                if n == myresult[i][0]:
                    n2 = input("Pls Enter the date till which you will be staying (Format: YYYY-MM-DD): ")
                    sql = "UPDATE rooms SET Booked_Till = \""+n2+"\",Availability = \"Not Available\",Booked_By = \""+mail+"\" WHERE Room_No = \""+n+"\""
                    mycursor.execute(sql)
                    mydb.commit()
                    mycursor.execute("SELECT Cur_Bookings FROM non_subs WHERE EmaiL_ID  = \"Harry@gmail.com\"")
                    l = ""
                    myresult2 = mycursor.fetchall()
                    if myresult2 != []:
                        for i in range (0,len(myresult)):
                            l = l+","+myresult2[i]
                    l = l+","+n
                    sql = "UPDATE subs_users SET Cur_Bookings = \""+ l + "\" WHERE Email_ID = \""+mail+"\""
                    mycursor.execute(sql)
                    mydb.commit()
                    sql = "SELECT Room_Type FROM rooms WHERE Room_No = (%s)"
                    val = [n,]
                    mycursor.execute(sql,val)
                    myresult3 = mycursor.fetchone()
                    pr = "Your "+ str(myresult3[0])+" has been booked. "
                    print(pr)
                    sql = "SELECT Price_per_Night FROM rooms WHERE Room_No = (%s)"
                    val = [n,]
                    mycursor.execute(sql,val)
                    myresult4 = mycursor.fetchone()[0]
                    sql = "SELECT Sub_Type FROM subs_users WHERE Email_ID = (%s)"
                    val = (mail,)
                    mycursor.execute(sql,val)
                    myresult5 = mycursor.fetchone()[0]
                    if myresult5 == "Silver":
                        myresult4 *= 93/100
                        off = "7%"
                    elif myresult5 == "Gold":
                        myresult4 *= 85/100
                        off = "15%"
                    elif myresult5 == "Platinum":
                        myresult4 *= 80/100
                        off = "20%"
                    elif myresult5 == "Diamond":
                        myresult4 *= 75/100
                        off = "25"
                    pr1 = "Since you have a "+myresult5+" subscription, you have availed "+off+" off."
                    pr2 = "Please do your payment according to ("+str(myresult4)+" per night) at the time of your arrival."
                    print(pr1)
                    print(pr2)
                    print("Hope you have a good stay.")
                    Sub_User_Dashboard(mail,pw)
    else:
        dt = input("Pls Enter Date when you want to stay (Format: YYYY-MM-DD): ")
        sql = "SELECT Room_No, Room_Type, Price_per_Night, Features FROM rooms WHERE Booked_Till < \""+dt+"\""
        mycursor.execute(sql)
        mydb.commit()
        myresult = mycursor.fetchall()
        print("Available Rooms ")
        for x in myresult:
            print("Room",x[0],": ",x[1])
            print("      Features: ",x[3])
            print("      Price per night: ",x[2])
        print("")
        while True:
            n = input("Pls Enter the Room_No of the Room which you would like to book: ")
            for i in range(0,len(myresult)):
                if n == myresult[i][0]:
                    n2 = input("Pls Enter the date till which you will be staying (Format: YYYY-MM-DD): ")
                    sql = "UPDATE rooms SET Booked_Till = \""+n2+"\",Availability = \"Not Available\",Booked_By = \""+mail+"\" WHERE Room_No = \""+n+"\""
                    mycursor.execute(sql)
                    mydb.commit()
                    mycursor.execute("SELECT Cur_Bookings FROM non_subs WHERE EmaiL_ID  = \"Harry@gmail.com\"")
                    l = ""
                    myresult2 = mycursor.fetchall()
                    if myresult2 != []:
                        for i in range (0,len(myresult)):
                            l = l+","+myresult2[i]
                    l = l+","+n
                    sql = "UPDATE non_subs SET Cur_Bookings = \""+ l + "\" WHERE Email_ID = \""+mail+"\""
                    mycursor.execute(sql)
                    mydb.commit()
                    sql = "SELECT Room_Type FROM rooms WHERE Room_No = (%s)"
                    val = [n,]
                    mycursor.execute(sql,val)
                    myresult3 = mycursor.fetchone()
                    pr = "Your "+ str(myresult3[0])+" has been booked. "
                    print(pr)
                    sql = "SELECT Price_per_Night FROM rooms WHERE Room_No = (%s)"
                    val = [n,]
                    mycursor.execute(sql,val)
                    myresult4 = mycursor.fetchone()
                    pr = "Please do your paymeny according to ("+str(myresult4[0])+" per night) at the time of your arrival."
                    print(pr)
                    print("Hope you have a good stay.")
                    
                    NonSub_User_Dashboard(mail,pw)

def Change_Info(mail,pw,s):
    print("")
    n = int(input("1.Change Name \n2.Change Password \n3.Go Back \nEnter: "))
    if n==1:
        Change_Name(mail,pw,s)
    elif n==2:
        Change_Password(mail,pw,s)
    elif n==3:
        Subs_User_Dashboard(mail,pw,s)
    else:
        print("Wrong Input. Pls Enter Again")
        Change_Info(mail,pw,s)

def Change_Name(mail,pw,s):
    print("")
    name = input("Pls Enter your New Name: ")
    if s == "subs":
        sql = "UPDATE subs_users SET Name = \""+name+"\" WHERE Email_ID = \""+mail+"\""
        mycursor.execute(sql)
        mydb.commit()
    else:
        sql = "UPDATE non_subs SET Name = \""+name+"\" WHERE Email_ID = \""+mail+"\""
        mycursor.execute(sql)
        mydb.commit()

def Change_Password(mail,pw,s):
    pw = input("Pls Enter your New Password: ")
    if s == "subs":
        sql = "UPDATE subs_users SET Password = \""+pw+"\" WHERE Email_ID = \""+mail+"\""
        mycursor.execute(sql)
        mydb.commit()
    else:
        sql = "UPDATE non_subs SET Password = \""+pw+"\" WHERE Email_ID = \""+mail+"\""
        mycursor.execute(sql)
        mydb.commit()

def Rec_Pw(mail,s):
    print("")
    n = int(input("1.Last Password \n2.Security Question \n3.Go Back \nEnter: "))
    if n==1:
        pw = input("Enter Last Password you remember using with this account: ")
        if s == "sub":
            sql = "SELECT Cust_ID FROM subs_users WHERE Email_ID = (%s)"
            val = (mail,)   
            mycursor.execute(sql,val)
            myresult = mycursor.fetchone()[0]
            sql = "SELECT Old_PW FROM subs_user_rec WHERE Cust_ID = (%s)"
            val = (myresult,)
            mycursor.execute(sql,val)
            myresult = mycursor.fetchone()[0]
            if pw == myresult:
                pw1 = input("Please Enter the New Password: ")
                sql = "UPDATE subs_users SET Password = (%s) WHERE Email_ID = \""+mail+"\""
                val = (pw1,)
                mycursor.execute(sql,val)
                mydb.commit()
            else:
                print("Incorrect Password.")
                Rec_Pw(mail,s)
        else:
            sql = "SELECT Cust_ID FROM non_subs WHERE Email_ID = (%s)"
            val = (mail,)   
            mycursor.execute(sql,val)
            myresult = mycursor.fetchone()[0]
            sql = "SELECT Old_PW FROM user_rec WHERE Cust_ID = (%s)"
            val = (myresult,)
            mycursor.execute(sql,val)
            myresult = mycursor.fetchone()[0]
            if pw == myresult:
                pw1 = input("Please Enter the New Password: ")
                sql = "UPDATE non_subs SET Password = (%s) WHERE Email_ID = \""+mail+"\""
                val = (pw1,)
                mycursor.execute(sql,val)
                mydb.commit()
            else:
                print("Incorrect Password.")
                Rec_Pw(mail,s)

    elif n==2:
        
        if s == "sub":
            sql = "SELECT Hint,Hint_Ans FROM subs_users_rec WHERE Email_ID = (%s)"
            val = (mail,)   
            mycursor.execute(sql,val)
            myresult = mycursor.fetchone()
            print(myresult[0])
            ans = input("Enter your answer: ")
            if ans.strip() == myresult[1]:
                pw1 = input("Please Enter the New Password: ")
                sql = "UPDATE subs_users SET Password = (%s) WHERE Email_ID = \""+mail+"\""
                val = (pw1,)
                mycursor.execute(sql,val)
                mydb.commit()
            else:
                print("Incorrect Answer.")
                Rec_Pw(mail,s)        

        else:
            sql = "SELECT Hint,Hint_Ans FROM user_rec WHERE Email_ID = (%s)"
            val = (mail,)   
            mycursor.execute(sql,val)
            myresult = mycursor.fetchone()
            print(myresult[0])
            ans = input("Enter your answer: ")
            if ans.strip() == myresult[1]:
                pw1 = input("Please Enter the New Password: ")
                sql = "UPDATE non_subs SET Password = (%s) WHERE Email_ID = \""+mail+"\""
                val = (pw1,)
                mycursor.execute(sql,val)
                mydb.commit()
            else:
                print("Incorrect Answer.")
                Rec_Pw(mail,s)
                
    elif n==3:
            Login()
            
    else:
        print("Wrong Input.")
        Rec_Pw(mail,s)

def Logout():
    mail = ""
    pw = ""
    s = ""
    print("\nSuccessfully Loged Out. \nRedirecting to Home Page")
    start()

start()

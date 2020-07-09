import smtplib
import msvcrt

urlList=['http:','https:','www.','/']
urlList1=['->']
urlList2=['//']
sendOne=True
recipientNo=0

credentials = open('credentials.txt','r')
writeMail = open('writeMail.txt','r')
idPwd = credentials.readlines()
emailLine = writeMail.readlines()

gmailUser = idPwd[0].split(':')[1]
gmailPassword = idPwd[1].split(':')[1]
eSubject= emailLine[0].split(':')[1]
eBody=''.join(emailLine[1:])
credentials.close()
writeMail.close()
sentFrom = str(gmailUser.strip())
subject = str(eSubject.strip())
body = str(eBody.strip())
toAll=[]
toPrevious=[]
emailText = """\
From: %s
Subject: %s
%s
""" % (sentFrom, subject, body)

def Help():
    print('\nHere are the steps to make this work:\n\nStep1: Read all the .txt files and follow the given instructions.\nStep2: Now, run the script and you can choose the type of execution you want.\nStep3: Thank me by sending a mail using this script at therealcybergeek@gmail.com XD')
    print('\nCommonly Known Issues:\n\nGoogle prevents logging in from unknown sources and less secure apps (including this script)\nthus preventing this application from sending emails.\nVisit https://myaccount.google.com/lesssecureapps and enable access from less secure apps.\n\nDisable two factor authorisation in your gmail account for this script to work.\n\nAs Max Limit for bcc in Gmail using this script is 100\nso keep this in mind (Total Recipients Per Mail=Number Of Recipients x Number Of Recipient Formats)')
    input()

def request():
    global toPrevious, toAll, domain, count, recipientNo
    count=0
    bcc=recipientNo*len(open('recipientFormats.txt','r').readlines())
    recipient = open('recipient.txt', 'r')
    for domain in recipient:
        count += 1
        if any(urlParts in domain for urlParts in urlList1):
            domain=domain.split('->')[1]
        if any(urlParts in domain for urlParts in urlList2):
            domain=domain.split('/')[2]
        for urlParts in urlList:
            domain=domain.replace(urlParts,'')
            domain=str(domain.strip())

        print(str(count)+'-> '+domain+'\n')
        if sendOne==True:
            print('Press Enter to Send Mail to this Recipient or Press Space to Skip')
            userInput=msvcrt.getch()
            if userInput!=b' ':
                print('Sending...')
                recipientFormats = open('recipientFormats.txt','r')
                toRecipient=[]
                for formatLine in recipientFormats:
                    toRecipient.append(formatLine.split(':')[0].strip()+domain+formatLine.split(':')[2].strip())
                recipientFormats.close()
                sendMails(toRecipient, domain, count)
            else:
                print('Recipient Skipped: '+domain+'\n')
        else:
            recipientFormats = open('recipientFormats.txt','r')
            toRecipient=[]
            for formatLine in recipientFormats:
                toRecipient.append(formatLine.split(':')[0].strip()+domain+formatLine.split(':')[2].strip())
            recipientFormats.close()
            toAll.extend(toRecipient)
            if len(toAll)%bcc==0:
                toCurrent=diff(toAll, toPrevious)
                toPrevious.extend(toAll)
                print('Mail Recipients('+str(bcc)+'):\n')
                print(toCurrent)
                print('\nPress Enter to Send Mails to these '+str(recipientNo)+' recipients or Press Space to Skip')
                userInput=msvcrt.getch()
                if userInput!=b' ':
                    print('Sending Mail to these recipients...')
                    sendMails(toCurrent, domain, count)
                else:
                    print('Mail Skipped\n')
    recipient.close()
    if sendOne==True:
        print('Done!')
    else:
        toCurrent=diff(toAll, toPrevious)
        if toCurrent!=[]:
            print('Mail Recipients('+str(len(toCurrent))+'):\n')
            print(toCurrent)
            print('\nPress Enter to Send Mails to these '+str(recipientNo)+' recipients or Press Space to Skip')
            userInput=msvcrt.getch()
            if userInput!=b' ':
                print('Sending Mail to these recipients...')
                sendMails(toCurrent, domain, count)
            else:
                print('Mail Skipped\nDone!')
    input('Press Enter to Exit')

def diff(toAll, toPrevious):
    toCurrent = [i for i in toAll + toPrevious if i not in toAll or i not in toPrevious]
    return toCurrent
    
def sendMails(to, domain, count):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmailUser, gmailPassword)
        server.sendmail(sentFrom, to, emailText)
        server.close()
        if sendOne==True:
            print('Email sent to recipient'+str(count)+' '+domain+'\n')
        else:
            print('\nEmail sent to '+str(recipientNo)+' recipients')
            print('Done!')
    except:
        if sendOne==True:
            print('Something went wrong...\nEmail not sent to recipient'+str(count)+' '+domain+'\n')
        else:
            print('\nSomething went wrong...\nEmail not sent to these '+str(recipientNo)+' recipients')

print('Welcome to Send Mails!\nPress Enter to Send Mails one by one to recipients / Press Space to Send Mail to All recipients / Press H for help')
userInput=msvcrt.getch()
if userInput==b'h':
    Help()
elif userInput==b' ':
    sendOne=False
    recipientNo=int(input('\n(Total Recipients Per Mail=Number Of Recipients x Number Of Recipient Formats)\nEnter Number of Recipient per Mail (Max=25): '))
    print('\nSending Mails to '+str(recipientNo)+' Recipients per Mail\n')
    request()
else:
    print('\nSending Mails One by One to Recipients\n')
    request()



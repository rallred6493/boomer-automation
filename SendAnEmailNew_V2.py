import win32com.client
import pandas as pd

#Global Dictionaries/Lists
Emails = {'BHPM': 'joy.wachendorf@blackhillscorp.com', 'BPAP': 'bpapatf@bpa.gov', 'BRTM': 'settlementwc@brookfieldrenewable.com', 
    'BURBT': 'BurbankSettlements@burbankca.gov','CRSPM': 'MTFirmCkOut@wapa.gov',
    'CCG': 'Michael.Zito@constellation.com;CCGPowerPayments@constellation.com', 'CORPW': 'shalena.armstrong@shell.com',  'DYNP': 'anazkhan@dynastypower.ca;confirms@dynastypower.ca', 
    'EDF': 'PowerAcctg@edftradingna.com', 'ENKP': 'settlements@energykeepersinc.com', 'GLNDGL': 'Settlements-Bilateral@acespower.com', 'LAWM': 'yiu.pang@ladwp.com', 
    'PAC': 'paccheckout@pacificorp.com', 'PRPM': 'PRPACheckouts@prpa.org', 'PSCO': 'caitlynn.r.barber@xcelenergy.com;pscopurchasepower@xcelenergy.com;joshua.t.ford@xcelenergy.com', 'MSCG': 'commodpsg@morganstanley.com;sushil.bhalerao@morganstanley.com', 'REMC': 'powercheckouts@rainbowenergy.com',
    'STG': 'nathan.kirkland@sgcity.org;brian.jeppson@sgcity.org', 'TEMUWS': 'TransAlta_Settlements@TransAlta.com', 'TENASKA': 'sguerra@tnsk.com;ebruce@tnsk.com', 'TSPMTS': 'cgroce@tristategt.org',
    'UAMPTS': 'prescheduling@uamps.com', 'UGC': 'UGCNAsettlements@uniper.energy', 'AEPCA': 'Settlements-Bilateral@acespower.com', 'MCPI': 'MOTMODSettlementsPowerHouston@macquarie.com'} 
#Counterparties that are Pacific Prevailing Time
PPT = ['AEPCA','BPAP', 'BRTM', 'BURBT', 'CCG','DYNP','EDF','ENKP','GLNDGL','LAWM','MCPI','MSCG','PAC','PSCO','REMC','TEMUWS','TENASKA','UAMPTS','UGC','BPAP','CORPW', 'CRSPM']

#Counterparties that are Mountain Prevailing Time
MPT = ['BHPM','STG','PRPM','TSPMTS']

#Use this list for counterparties that have already sent their monthly checkout email.
SKIP = ['PRPM','BHPM','CISO', 'CRSPM']

def main():

    #Download both MPT and PPT versions of Global Settlement by Counterparty
    ppt = "C:\\Users\\RachelAllred\\OneDrive - Utah Municipal Power Agency\\Python\\CounterPartyCheckout\\PPT.csv"
    mpt = "C:\\Users\\RachelAllred\\OneDrive - Utah Municipal Power Agency\\Python\\CounterPartyCheckout\\MPT.csv"
    ppt = sendEmailPPT(ppt)
    mpt = sendEmailMPT(mpt)

def sendEmailPPT(fileName):
    #Load in global counterparties csv
    #skiprows will be anywhere from 8-10 depending on which filters are applied. The more filters applied the higher the number
    df = pd.read_csv(fileName, skiprows=9)

    #Find month and year for the subject line of the email
    #Do number of rows-3-skiprowsvalue to figure out what to put in the row section for date df[Row][HERE][:10]
    date = df["Counterparty"][19][:10]
    print(date)
    month = str(int(date[1:2]) -1) 
    year = date[6:]
    


    df = df.head(-3)
    df = df.rename(columns={"Full Name": "Name", "MW Sold Total": "MWSold", "Energy Sold Total": "EnergySold", "MW Purchased Total": "MWPurchased", "Energy Purchased Total": "EnergyPurchased"})
    
    for i in df.index:
        counterparty = ''.join((element for element in df['Counterparty'][i] if not element.isdigit()))
        
        #Only run for PPT counterparties. Do not include MPT or SKIP counterparties
        if counterparty in MPT or counterparty in SKIP:
            continue
        print(counterparty +" is PPT.")
        message = "Hi,\n\nHope your day is going well! Please let me know if you agree:\n\n"
        htmlMessage = "Hi,<br><br>Hope your day is going well! Please let me know if you agree:"

        #check for sales
        if str(df['MWSold'][i]) != "nan": #SALES
            message += "UMPA sold " + str(df['MWSold'][i]) + " MWs for $" + str(df['EnergySold'][i][1:]) + ".\n"
            htmlMessage += "<br><br>UMPA sold " + str(df['MWSold'][i]) + " MWs for $" + str(df['EnergySold'][i][1:]) + "."
        else:
            message+=""
            htmlMessage += ""

    #check for purchases
        if str(df['MWPurchased'][i]) != "nan": #Purchases
            message+="UMPA purchased " + str(df['MWPurchased'][i][1:]) + " MWs for $" + str(df['EnergyPurchased'][i]) + ".\n"
            htmlMessage += "<br><br>UMPA purchased " + str(df['MWPurchased'][i][1:]) + " MWs for $" + str(df['EnergyPurchased'][i]) + "."
        else:
            message+=""
            htmlMessage += ""

        htmlMessage+= "<br><br>Thanks,<br>"
        subject = "UMPA\\"+ counterparty + " Monthly Settlement " + month + "-" + year
        recipient = Emails[counterparty]
        #print(Emails[counterparty])
        sendEmail(htmlMessage, subject, recipient)
        # if i==0:
        #     break

def sendEmailMPT(fileName):
    #Load in global counterparties csv
    df = pd.read_csv(fileName, skiprows=8)
    

    #Find month and year for the subject line of the email
    date = df["Counterparty"][19][:10]
    month = str(int(date[1:2]) -1) 
    year = date[6:]

    df = df.head(-3)
    df = df.rename(columns={"Full Name": "Name", "MW Sold Total": "MWSold", "Energy Sold Total": "EnergySold", "MW Purchased Total": "MWPurchased", "Energy Purchased Total": "EnergyPurchased"})
    
    for i in df.index:
        counterparty = ''.join((element for element in df['Counterparty'][i] if not element.isdigit()))
        if counterparty in PPT or counterparty in SKIP:
            continue
        print(counterparty+ " is MPT.")
        message = "Hi,\n\nHope your day is going well! Please let me know if you agree:\n\n"
        htmlMessage = "Hi,<br><br>Hope your day is going well! Please let me know if you agree:"

        #check for sales
        if str(df['MWSold'][i]) != "nan": #SALES
            message += "UMPA sold " + str(df['MWSold'][i]) + " MWs for $" + str(df['EnergySold'][i][1:]) + ".\n"
            htmlMessage += "<br><br>UMPA sold " + str(df['MWSold'][i]) + " MWs for $" + str(df['EnergySold'][i][1:]) + "."
        else:
            message+=""
            htmlMessage += ""

    #check for purchases
        if str(df['MWPurchased'][i]) != "nan": #Purchases
            message+="UMPA purchased " + str(df['MWPurchased'][i][1:]) + " MWs for $" + str(df['EnergyPurchased'][i]) + ".\n"
            htmlMessage += "<br><br>UMPA purchased " + str(df['MWPurchased'][i][1:]) + " MWs for $" + str(df['EnergyPurchased'][i]) + "."
        else:
            message+=""
            htmlMessage += ""

        htmlMessage+= "<br><br>Thanks,<br>"
        subject = "UMPA\\"+ counterparty + " Monthly Settlement " + month + "-" + year
        recipient = Emails[counterparty]
        #print(Emails[counterparty])
        sendEmail(htmlMessage, subject, recipient)
        # if i==0:
        #     break

#Function used to create the Outlook item and Display and/or Send it
def sendEmail(message, subject, recipient):
    outlook = win32com.client.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = recipient
    mail.Subject = subject
    mail.GetInspector

    index = mail.HTMLBody.find('>', mail.HTMLBody.find('<BODY')) 
    mail.HTMLBody =  message + mail.HTMLBody[:index + 1] 

    #Displays the message
    mail.Display()

    #Sends the message automatically
    #mail.Send()
    print(recipient + "\n" + subject + "\n"+ message)


if __name__ == main():
    main()
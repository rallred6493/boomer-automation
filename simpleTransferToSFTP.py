import pysftp as s

localFile = 'C:\\Users\\RachelAllred\\OneDrive - Utah Municipal Power Agency\\PCI\\MV90_5M_Billing__20220616150609.csv'
RemoteLocation = '/METERDATA_INPUT/5Minute_MV90_Billing'
hostname = 'umpa-fs.powercosts.com'
username = 'pciumpa-mt-p-ftp'
password = '8wDud35As05qRuFA'

#disable hostkey checking as we alternate through different hostkeys
cnopts = s.CnOpts()
cnopts.hostkeys = None

with s.Connection(host=hostname, username=username, password=password, cnopts=cnopts, port=443) as conn:
    print("Connection Established!")
    with conn.put(localFile, RemoteLocation):
        print(localFile + " successfully transferred!")

import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import os
from datetime import datetime

def main():
    listOfFiles = fileSelection()
    loaddf = pd.DataFrame(columns = ['MeterName', 'Edition', 'BeginDate', 'TimeZone', 'Net', 'Quality'])
    gendf = pd.DataFrame(columns = ['MeterName', 'Edition', 'BeginDate', 'TimeZone', 'Net', 'Gross', 'Aux', 'Quality'])
    for filepath in listOfFiles:
        print(filepath)
        df = pd.read_csv(filepath)
        meterName, genorload = assignPCIName(filepath)
        
        edition = 'Verified'
        timezone = 'GMT-07:00'
        quality = 'G'
        
        if genorload == 1:
            for row in df.index:
                beginDate = df['StartDate'][row]
                mws = df['Value'][row]

                loaddf = loaddf.append({'MeterName': meterName, 'Edition': edition, 'BeginDate': beginDate, 'TimeZone': timezone, 'Net': mws, 'Quality': quality}, ignore_index=True)
        elif genorload == 0:
            for row in df.index:
                beginDate = df['StartDate'][row]
                mws = df['Value'][row]

                gendf = gendf.append({'MeterName': meterName, 'Edition': edition, 'BeginDate': beginDate, 'TimeZone': timezone, 'Net': mws, 'Quality': quality, 'Gross': mws, 'Aux': 0}, ignore_index=True)
        else:
            print("Sucks to suck.")

    genFilePath =  'C:\\Users\\RachelAllred\\OneDrive - Utah Municipal Power Agency\\PCI\\Meters\\Import Files\\genData.csv'
    loadFilePath =  'C:\\Users\\RachelAllred\\OneDrive - Utah Municipal Power Agency\\PCI\\Meters\\Import Files\\loadData.csv'
    gendf.to_csv(genFilePath)
    loaddf.to_csv(loadFilePath)


    # print(df)
def fileSelection():
    files = []
    #single file UNCOMMENT FOR SINGLE FILE
    # filepath = 'C:\\Users\\RachelAllred\\Utah Municipal Power Agency\\File Share - General\\2 Operations\\Meter Data\\Jem Reads\\Jem Edits\\NEW_SalemArrowProf11260502.csv'
    # files.append(filepath)

    #files in a certain location
    filePath = 'C:\\Users\\RachelAllred\\Utah Municipal Power Agency\\File Share - General\\2 Operations\\Meter Data\\Jem Reads\\May012022-May312022'

    #Loops through all files in specified file path
    for file in os.listdir(filePath):
        #Create file path
        fileWithPath = os.path.join(filePath, file)
        timeFloat = os.path.getmtime(fileWithPath)
        time = datetime.fromtimestamp(timeFloat).strftime('%Y-%m-%d')

        if file.startswith('NEW_'):
            files.append(fileWithPath)

    return files

# def dfFromFile(df, meterName, edition, timezone, quality, genorload):
#     newdf = pd.DataFrame(columns = ['MeterName', 'Edition', 'BeginDate', 'TimeZone', 'Net', 'Quality'])
#     for row in df.index:
#         beginDate = df['StartDate'][row]
#         mws = df['Value'][row]

#         newdf = newdf.append({'MeterName': meterName, 'Edition': edition, 'BeginDate': beginDate, 'TimeZone': timezone, 'Net': mws, 'Quality': quality}, ignore_index=True)
#     return newdf

def assignPCIName(filepath):
    split = filepath.split('\\')
    meterUMPA = split[9]
    meter = meterUMPA[4:-12]

    #0 = gen meter and 1 = load meter
    if meter == 'SalemLoaferProf':
        name = 'SA_LOAFER_SUB'
        genorload = 1
    elif meter == 'BMB6MileProf':
        name = 'SIX_MILE_HYDRO'
        genorload = 0
    elif meter == 'Hale 2Prof':
        name = 'PV_HALE 2_IMPORT'
        genorload = 1
    elif meter == 'OlmsteadProf':
        name = 'OLMSTED_HYDRO'
        genorload = 0
    elif meter == 'LevanCobbleProf':
        name = 'LEVAN_COBBLE_ROCK'
        genorload = 0
    elif meter == 'LevanProf':
        name = 'LEVAN_IMPORT'
        genorload = 1
    elif meter == 'NephiProf':
        name = 'NEPHI_IMPORT'
        genorload = 1
    elif meter == 'MantiLowerProf':
        name = 'MANTI_LOWER'
        genorload = 0
    elif meter == 'MantiProf':
        name = 'MANTI_IMPORT'
        genorload = 1      
    elif meter == 'NephiBradleyProf':
        name = 'NEPHI_BRADLEY'
        genorload = 0
    elif meter == 'SalemArrowProf':
        name = 'SA_ARROWHEAD_SUB'
        genorload = 1
    elif meter == 'SFWhiteheadProf':
        name = 'SF_WHITEHEAD_SUB'
        genorload = 1
    elif meter == 'SFDCWhiteheadProf':
        name = 'SF_DC_WHITEHEAD_2_SUB'
        genorload = 1
    elif meter == 'SFCanyonProf':
        name = 'SF_CANYON_SUB'
        genorload = 1
    elif meter == 'Hale 1Prof':
        name = 'PV_HALE_GILL_1 CB110_IMPORT'
        genorload = 1
    elif meter == 'MantiUpperProf':
        name = 'MANTI_UPPER'
        genorload = 0
    elif meter == 'NephiProf':
        name = 'NEPHI_IMPORT'
        genorload = 1
    elif meter == 'LevanPigeonProf':
        name = 'LEVAN_PIGEON_CREEK'
        genorload = 0
    elif meter == 'LevanProf':
        name = 'LEVAN_IMPORT'
        genorload = 1
    elif meter == 'SFDCWoodhouseProf':
        name = 'SF_DRYCREEK_SUB'
        genorload = 1
    elif meter == 'BYUCOGENProf':
        name = 'BYU_COGEN'
        genorload = 0
    elif meter == 'TannerProf':
        name = 'PV_TANNER_IMPORT'
        genorload = 1
    elif meter == 'Clover CreekProf':
        name = 'CLOVER_CREEK_SLR'
        genorload = 0
    elif meter == 'NephiSaltCreekProf':
        name = 'NEPHI_SALT_CREEK'
        genorload = 0
    elif meter == 'SF Comm SolarProf':
        name = 'SF_COMM_SOLAR'
        genorload = 0
    else:
        name = meter

    return name, genorload
main()
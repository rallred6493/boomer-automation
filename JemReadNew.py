import pandas as pd
from mod import Mod
import os
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

def main():

    # # Use this and comment out the rest if you need to adjust a specific file
    # filePath = 'C:\\Users\\RachelAllred\\Utah Municipal Power Agency\\File Share - General\\2 Operations\\Meter Data\\Jem Reads\\March312022-April302022\\SalemArrowProf11260502.csv'
    # updateJem(filePath)

    #Use this section of code if you would like to run the program on all files in the UA\Downloads Folder
    files =[]
    # filePath = 'C:\\Users\\RachelAllred\\OneDrive - Utah Municipal Power Agency\\Python\\JemReadReview\\Files That Don\'t Work\\'
    filePath = 'C:\\Users\\UA\\Downloads\\'

    # #Loops through all files in specified file path
    for file in os.listdir(filePath):
        #Create file path
        fileWithPath = os.path.join(filePath, file)
        timeFloat = os.path.getmtime(fileWithPath)
        time = datetime.fromtimestamp(timeFloat).strftime('%Y-%m-%d')

        #Append File Path to list of files to be parsed
        if time == '2022-06-14':
            files.append(fileWithPath)
    
    #Call the updateJem function on every file in the files list
    for path in files:
        updateJem(path)

def updateJem(filepath):

    #Separate to find the file name and use the file name to find the meter name
    split = filepath.split('\\')
    filename = split[4]
    file = pd.read_csv(filepath,skiprows = 4)
    meter = filename[:-12]

    print("Parsing "+ filename)

    #Each file has a similar format, but some are slightly different. This code adjusts each file so that we have relevant info, RecordNum, Events, Dates, and MWs.
    if meter == 'SF Comm SolarProf':
        multiplier = 0.00022
        file.columns = ['RecordNum', 'Event', 'StartDate', 'EndDate', '3', '1', '2', 'MW', '4','5','6']
        file = file.drop(['1','2','3','4','5','6'], axis=1)        
    elif len(file.columns) == 13:
        file.columns = ['RecordNum', 'Event', 'StartDate', 'EndDate', 'MW', '1', '2', '3', '4','5','6','7','8']
        file = file.drop(['1','2','3','4','5','6','7','8'], axis=1)
    elif len(file.columns) == 9:
        file.columns = ['RecordNum', 'Event', 'StartDate', 'EndDate', 'MW', '1', '2', '3', '4']
        file = file.drop(['1','2','3','4'], axis=1)
    elif len(file.columns) == 8:
        file.columns = ['RecordNum', 'Event', 'StartDate', 'EndDate', 'MW', '1', '2', '3']
        file = file.drop(['1','2','3'], axis=1)       
    else:
        file.columns = ['RecordNum', 'Event', 'StartDate', 'EndDate', 'MW', '1', '2', '3', '4','5','6']
        file = file.drop(['1','2','3','4','5','6'], axis=1)

    #Finds the multiplier for each meter
    if meter == 'SalemLoaferProf':
        multiplier = 0.000135
    elif meter == 'BMB6MileProf':
        multiplier = 0.0001
    elif meter == 'Hale 2Prof':
        multiplier = .00105
    elif meter == 'OlmsteadProf':
        multiplier = .0125
    elif meter == 'LevanCobbleProf':
        multiplier = 0.000005
    elif meter == 'LevanProf':
        multiplier = 0.0003
    elif meter == 'NephiProf':
        multiplier = 0.001
    elif meter == 'MantiLowerProf':
        multiplier = 0.001
    elif meter == 'MantiProf':
        multiplier = 0.00032      
    elif meter == 'NephiBradleyProf':
        multiplier = 0.00001
    elif meter == 'SalemArrowProf':
        multiplier = 0.0004
    elif meter == 'SFWhiteheadProf':
        multiplier = 0.0002
    elif meter == 'SFDCWhiteheadProf':
        multiplier = 0.000345
    elif meter == 'SFCanyonProf':
        multiplier = 0.00036
    elif meter == 'Hale 1Prof':
        multiplier = 0.0021
    elif meter == 'MantiUpperProf':
        multiplier = 0.0001125
    elif meter == 'NephiProf':
        multiplier = 0.001
    elif meter == 'LevanPigeonProf':
        multiplier = 0.00004
    elif meter == 'LevanProf':
        multiplier = 0.0003
    elif meter == 'SFDCWoodhouseProf':
        multiplier = 0.000345
    elif meter == 'BYUCOGENProf':
        multiplier = 0.00027
    elif meter == 'TannerProf':
        multiplier = 0.0021
    elif meter == 'Clover CreekProf':
        multiplier = 0.00388
    elif meter == 'NephiSaltCreekProf':
        multiplier = 0.0001
    elif meter == 'SF Comm SolarProf':
        multiplier == 0.00022
    else:
        print("SOS! You are missing "+ meter)
    file = file.dropna()
    #check each row for freeze or other event that needs attention.
    for row in file.index:

        #Normal file events, no action needed.
        if file['Event'][row] == ' Normal' or file['Event'][row] == 'Midnight' or file['Event'][row] == 'BPRMidnight' or file['Event'][row] == ' MidnightNormal':
            count = 1
            continue
        
        #Freeze math.
        elif file['Event'][row] == 'Freeze' or file['Event'][row] == ' Freeze':
            print("Freeze found @ "+ file['StartDate'][row])
            before = int(file['EndDate'][row-count][13:-5])
            after = int(file['StartDate'][row+1][13:-5])
            
            if before == 0 or Mod(before, 5) == 0:
                print("Freeze math is after.")
                file['MW'][row+1] = int(file['MW'][row]) + int(file['MW'][row+1])
                file = file.drop(row)

            elif after == 0 or Mod(after,5) == 0:
                print("Freeze math is before.")
                file['MW'][row-count] = int(file['MW'][row]) + int(file['MW'][row-count])
                file = file.drop(row)
        #We have a few extra events that aren't consistent in their calculation. This code leaves a notfication that there is more action that needs to be taken.
        else:
            print(file['StartDate'][row]+"\nIncludes an unusual event, "+ file['Event'][row] +". Look into file further.")
        count += 1
    #Multiply each MW value by the multiplier to get the correct value        
    file['Value'] = round(file.apply(lambda row: int(row['MW'])*multiplier*12, axis =1),3)
    
    #Create new file
    newFilePath = 'C:\\Users\\RachelAllred\\Utah Municipal Power Agency\\File Share - General\\2 Operations\\Meter Data\\Jem Reads\\Jem Edits\\NEW_' + filename 
    file.to_csv(newFilePath)
    print("\n")

if __name__ == main():
    main()
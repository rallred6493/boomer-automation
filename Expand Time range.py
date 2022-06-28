import pandas as pd
#The way the data works, if the transmission row is 0 we are holding no reserves. This will always be on an hourly basis, meaning there are no weird
# subhourly ranges to deal with.

def main():
    #Open the energy profile from the TAG NSR0422
    df = pd.ExcelFile('C:\\Users\\RachelAllred\\OneDrive - Utah Municipal Power Agency\\Python\\APD Time Range\\Energy and Transmission Profile.xlsx')

    #Remove headings from dataframe
    df = df.parse('Sheet 1', skiprows=3)
    #Remove details of date and other items from the bottom of the dataframe
    df = df.iloc[:-5]
    
    #Used for testing, only goes through a selected number of rows instead of all of them.
    #count = 0

    #Go through every single row in the df
    for row in df.index:
        #Used for testing, only goes through a selected number of rows instead of all of them.
        # if count > 30:
        #     break

        #Change start time and end time into floats to calculate the difference between the two, i.e. 11:30 = 11.3
        start = float(df['Start'][row][0:2]) + float(df['Start'][row][3:])/100
        end = float(df['Stop'][row][0:2]) + float(df['Stop'][row][3:])/100

        #Store the Date of the row in this date variable
        date = df['Date'][row]
        print(date, start, end)
        difference = end - start

        #Handle all times when reserves are at 0.
        if df['Trans'][row] == 0:
            print("Expand time range. All values 0.")

            #If the difference is greater than 0, cycle through the range and give every single hour a MW value of 0
            if difference > 1:
                #Create a range from the start and end hours as integers
                for i in range(int(start), int(end)):
                    #Create temporary variables to store the date, start time, end time, and mws
                    new_date = df['Date'][row]
                    new_start = hour_into_time(i)
                    new_end = hour_into_time(i+1)
                    print(new_date, new_start, new_end)
                    #Add the new range of values to the dataframe
                    df.loc[len(df.index)] = [date, new_start, new_end, 0, 0, 0, 0,0,0]

            #If the difference is less than 0, that means our end time is HE24        
            elif difference < 0:
                for i in range(int(start), 24):
                    print("Time range includes HE24.")
                    new_date = df['Date'][row]
                    new_start = hour_into_time(i)
                    new_end = hour_into_time(i+1)
                    print(new_date, new_start, new_end) 
                    df.loc[len(df.index)] = [date, new_start, new_end, 0, 0, 0, 0,0,0]

            #Time Range is less than one hour and not negative!        
            else:
                print("Time range is less than one hour...")
        #Handle Time Ranges where reserves are not 0. Technically we only need the time ranges where the transmission is 0. So maybe create a new dataframe with the correct intervals?    
        else:
            print("Don't expand time range. Alter in Power BI.")
        
        #Used for testing
        # count += 1

    #Create new CSV file from dataframe
    df.to_csv('C:\\Users\\RachelAllred\\Downloads\\TagData.csv')
    
#Converts the number into time format
def hour_into_time(number):
    if number == 24:
        return "00:00"
    elif number < 10:
        return "0" + str(number) + ":00"
    else:
        return str(number) + ":00"
main()
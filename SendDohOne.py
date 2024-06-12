# Imports
import argparse
import requests as req
import datetime
import json
import os

# Constants
TEXT_COLOR_RED = "\033[31m"
TEXT_COLOR_GREEN = "\033[32m"
TEXT_COLOR_BLUE = "\033[34m"
TEXT_COLOR_RESET = "\033[0m"


REMOVE_SECONDS_FROM_DATE = -9
REVERSE_STRING_FOR_HEBREW = -1

PYTHON_SCRIPT_ROOT = (os.path.split(os.path.realpath(__file__)))[0]
JSON_DATABASE_NAME = "AuthKeys.json"
JSON_DATABASE_AUTHKEY = "AuthKey"
JSON_DATABASE_SUBMISSION_NAME = "SubmissionOptionDay"
JSON_DATABASE_KEYS = ["Name",JSON_DATABASE_AUTHKEY,"TimeStamp",fr"{JSON_DATABASE_SUBMISSION_NAME}1",fr"{JSON_DATABASE_SUBMISSION_NAME}2",fr"{JSON_DATABASE_SUBMISSION_NAME}3",fr"{JSON_DATABASE_SUBMISSION_NAME}4",fr"{JSON_DATABASE_SUBMISSION_NAME}5",fr"{JSON_DATABASE_SUBMISSION_NAME}6",fr"{JSON_DATABASE_SUBMISSION_NAME}7"]

URL_HOST = r"one.prat.idf.il"
URL_LOGIN = r"https://one.prat.idf.il/api/account/login"
URL_ATTENDANCE_OPTIONS = r"https://one.prat.idf.il:443/api/Attendance/GetAllFilterStatuses"
URL_ATTENDANCE_GET = r"https://one.prat.idf.il/api/Attendance/getFutureReport"
URL_ATTENDANCE_INSERT = r"https://one.prat.idf.il/api/Attendance/InsertFutureReport"

REFERER_LOGIN = r"https://one.prat.idf.il/login"
REFERER_SECONDARIES = r"https://one.prat.idf.il/secondaries"
REFERER_CALENDAR = r"https://one.prat.idf.il/calendar"
REFERER_HP = r"https://one.prat.idf.il/hp"

USER_AGENT = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"
ACCEPTED_DATA_TYPES = "application/json, text/plain, */*"
CONTENT_TYPE_MULTIPART = r"multipart/form-data; boundary=----WebKitFormBoundaryYYzAwUiDj80Dh1q1"
CONTENT_TYPE_APPLICATION = r"application/json;charset=UTF-8"

DOH_SUBMISSION_DATA = "\r\n------WebKitFormBoundaryYYzAwUiDj80Dh1q1\r\nContent-Disposition: form-data; name=\"MainCode\"\r\n\r\n{--A--}\r\n------WebKitFormBoundaryYYzAwUiDj80Dh1q1\r\nContent-Disposition: form-data; name=\"SecondaryCode\"\r\n\r\n{--B--}\r\n------WebKitFormBoundaryYYzAwUiDj80Dh1q1\r\nContent-Disposition: form-data; name=\"Note\"\r\n\r\n\r\n------WebKitFormBoundaryYYzAwUiDj80Dh1q1\r\nContent-Disposition: form-data; name=\"FutureReportDate\"\r\n\r\n{--C--}\r\n------WebKitFormBoundaryYYzAwUiDj80Dh1q1--\r\n"

# --------------------------------------------------------- #

# Microsoft Functions
# Generate Auth Key
def MicrosoftGenAuthKey():
    pass

# Retrieve The Auth Key from The Json Database
# Usage: MicrosoftGetAuthKey(123456789)
# Returns:
# vJsonProfiles[vID][AuthKey]   => Returns the Microsoft Authentication Key for The Specified vID
# False                         => if File/Profile/AuthKey Doesnt Exist, or if Fails openning the File
# Parameters:
# vID                           => the Profile ID Number
def MicrosoftGetAuthKey(vID):
        # Converting Parameters to Correct Type
    vID = str(vID)
    try:
        # Opening Json Database and Retrieving all Profiles
        with open(fr"{PYTHON_SCRIPT_ROOT}//{JSON_DATABASE_NAME}", "r") as f:
            vJsonProfiles = json.loads(f.read())
        # Only Return the AuthKey if Exists
        if (vJsonProfiles[vID][JSON_DATABASE_AUTHKEY] != ""):
            return vJsonProfiles[vID][JSON_DATABASE_AUTHKEY]
        return False
    except:
        return False

# Set The AuthKey for existing Profile in the Json Database
# Usage: MicrosoftSetAuthKey(123456789, <AuthenticationKey>)
# Returns:
# True          => if Set AuthKey Successfully
# False         => if Failed Setting AuthKey
# Parameters:
# vID           => the Profile ID Number
# vAuthKey      => Authentication Key for Specified Profile ID
def MicrosoftSetAuthKey(vID, vAuthKey):
    # Converting Parameters to Correct Type
    vID = str(vID); vAuthKey = str(vAuthKey)
    if (JsonSetProfile(vID, JSON_DATABASE_AUTHKEY, vAuthKey)):
        return True
    return False

# --------------------------------------------------------- #

# Json Database Functions
# Check if the Json Database exists
# Usage: JsonIsExist()
# Return:
# True          => if Exists
# False         => if doesnt Exist
# Parameters:   N/A
def JsonIsExist():
    if os.path.exists(f"{PYTHON_SCRIPT_ROOT}//{JSON_DATABASE_NAME}"):
        return True
    return False

# Creates a new Json Database
# Usage: JsonCreateFile(Force = True)
# Returns:
# True                      => if Created File
# False                     => if didnt Create File
# Parameters:
# vForce(Default = False)   => Overwrite Existing File
def JsonCreateFile(vForce = False):
    # Skip Creation if File Exist and Overwridden is not Requested
    if ((vForce != True) and JsonIsExist()):
        return False
    # Creating the Json Database File
    try:
        with open(fr"{PYTHON_SCRIPT_ROOT}//{JSON_DATABASE_NAME}", "w") as f:
            pass
        return True
    # Creation Failed
    except:
        return False

# Retrieve a Profile from the Json Database
# Usage: JsonGetProfile(123456789)
# Returns:
# vJsonProfiles     => Returns Specified ID Json Profile as dictionary if succeeded
# False             => if Requested Key doesnt exist or if Fails
# Parameters:
# vID               => the Profile ID Number
def JsonGetProfile(vID):
    # Converting Parameters to Correct Type
    vID = str(vID)
    try:
        # Retrieve Specified Profile Information
        with open(fr"{PYTHON_SCRIPT_ROOT}//{JSON_DATABASE_NAME}", "r") as f:
            vJsonProfiles = json.loads(f.read())
        # Fail if Database Empty
        if len(vJsonProfiles) == 0:
            return False
        return vJsonProfiles[str(vID)]
    except:
        return False
    
# Retrieve all Profiles from the Json Database
# Usage: JsonGetAllProfiles()
# Returns:
# vJsonProfiles     => Returns Specified ID Json Profile as dictionary if succeeded
# False             => if Requested Key doesnt exist or if Fails
# Parameters:       N/A
def JsonGetAllProfiles():
    try:
        # Retrieve Specified Profile Information
        with open(fr"{PYTHON_SCRIPT_ROOT}//{JSON_DATABASE_NAME}", "r") as f:
            vJsonProfiles = json.loads(f.read())
        # Fail if Database Empty
        if len(vJsonProfiles) == 0:
            return False
        return list(vJsonProfiles.keys())
    except:
        return False

# Change or Add Values to a Json Database Profile
def JsonSetProfile(vID, vKey, vValue, vChangingDays = False):
    # Converting Parameters to Correct Type
    vID = str(vID); vKey = str(vKey); vValue = str(vValue)

    # Exiting if Key doesnt Exist in Database "Template"
    if (not vChangingDays and vKey not in JSON_DATABASE_KEYS):
        return False
    # Exisiting if Day Doesnt Exist in Database Template
    elif(vChangingDays and fr"{JSON_DATABASE_SUBMISSION_NAME}{vKey}" not in JSON_DATABASE_KEYS):
        return False
    try:
        # Loading All Json Profiles
        with open(fr"{PYTHON_SCRIPT_ROOT}//{JSON_DATABASE_NAME}", "r") as f:
            vJsonProfiles = json.loads(f.read())
        # Setting Json Profile Value
        if vChangingDays:
            vJsonProfiles[vID][fr"{JSON_DATABASE_SUBMISSION_NAME}{vKey}"] = vValue
        else:
            vJsonProfiles[vID][vKey] = vValue
        # Writing Seetting
        with open(fr"{PYTHON_SCRIPT_ROOT}//{JSON_DATABASE_NAME}", "w") as f:
            json.dump(vJsonProfiles, f)
        return True
    
    # Setting Values Failed
    except:
        return False

# Create New Profile in Json Database
# Usage: JsonNewProfile(123456789)
# Returns:
# True          => if Succeeded at Adding Blank Profile to Json Database
# False         => if Succeeded at Adding Blank Profile to Json Database or Errors opening the File
# Parameters:
# vID           => the Profile ID Number
def JsonNewProfile(vID, vName):
    # Converting Parameters to Correct Type
    vID = str(vID); vName = str(vName)
    try:
        # Opening the Json Database and Reading all Profiles
        with open(fr"{PYTHON_SCRIPT_ROOT}//{JSON_DATABASE_NAME}", "r") as f:
            vJsonProfiles = f.read()
        if len(vJsonProfiles) != 0:
            vJsonProfiles = json.loads(vJsonProfiles)
        # Adding Another Blank Profile with all Required Keys as Blanks
        vProfilesDict = dict()
        for vKey in JSON_DATABASE_KEYS:
            vProfilesDict[vKey] = ""
        # Giving The Profile its Name
        vProfilesDict['Name'] = vName
        vProfilesDict['TimeStamp'] = str(datetime.datetime.now())
        vJsonProfiles[vID] = dict(vProfilesDict)
        # Writing the Blank Profile
        with open(fr"{PYTHON_SCRIPT_ROOT}//{JSON_DATABASE_NAME}", "w") as f:
            json.dump(vJsonProfiles, f)
        return True
    
    # Adding Blank Profile Failed
    except:
        return False

# Delete a Profile from The Json Database
# Usage: JsonDeleteProfile(123456789)
# Returns:
# True          => if Succeeded at Deleting Profile from Json Database
# False         => if Failed at Deleting Profile from Json Database or Profile Didnt Exist
# Parameters:
# vID           => the Profile ID Number
def JsonDeleteProfile(vID):
    # Converting Parameters to Correct Type
    vID = str(vID)
    try:
        # Opening the Json Database and Reading all Profiles
        with open(fr"{PYTHON_SCRIPT_ROOT}//{JSON_DATABASE_NAME}", "r") as f:
            vJsonProfiles = json.loads(f.read())
        # Deleting The Profile
        if not vJsonProfiles[vID]:
            return False
        vJsonProfiles.pop(vID, None)
        # Writing Back the Other Profiles
        with open(fr"{PYTHON_SCRIPT_ROOT}//{JSON_DATABASE_NAME}", "w") as f:
            json.dump(vJsonProfiles, f)
        return True
    
    # Deleting Profile Failed
    except:
        return False

# --------------------------------------------------------- #

# DohOne Functions
    
# Generate a Cookie to DohOne (prat.idf.il) Website
# Usage: DohOneGenCookie(123456789)
# Returns:
# vDohOneCookieData     => Returns The Actual DohOne Cookie Data
# False                 => if Didnt Retrieve The Desired Cookie for DohOne, or if Failed
# Parameters:
# vID                   => the Profile ID Number
def DohOneGenCookie(vID):
    # Converting Parameters to Correct Type
    vID = str(vID)
    try:
        # Retrieving The Correct AuthKey for the User from the Json Database
        vMicrosoftAuthKey = MicrosoftGetAuthKey(vID)

        # Requesting One Prat Cookies
        vDohOneRequest = req.get(URL_LOGIN, headers={"Authorization": vMicrosoftAuthKey, "Host": URL_HOST, "Referer": REFERER_LOGIN, "User-Agent": USER_AGENT})
        # Finding The Correct Cookie for DohOne and Returning The Cookie Data
        for vDohOneCookies in vDohOneRequest.cookies:
            if "Cookie AppCookie=" in str(vDohOneCookies):
                ###vDohOneCookieRaw = vDohOneCookies
                ###vDohOneCookie = str(vDohOneCookies).split(" ")[1]
                vDohOneCookieData = (str(vDohOneCookies).split(" ")[1]).split("=")[1]
                return vDohOneCookieData
        return False
    except:
        return False
    
# Send DohOne Report Submission
# Usage: DohOneSendFutureReport(123456789)
# Returns:
# True          => if Function Executed Successfully
# False         => if Something Broke
# Parameters:
# vID           => the Profile ID Number
def DohOneSendFutureReport(vID):
    # Converting Parameters to Correct Type
    vID = str(vID)
    
    try:
        # Retrieving Profile for Json Database
        vJsonProfile = JsonGetProfile(vID)
        # Creating a Dictionary with all Days of Week and Submission Option for each Day
        vSubmissionDayDict = dict()
        for vSubmissionDay in JSON_DATABASE_KEYS:
            if JSON_DATABASE_SUBMISSION_NAME not in vSubmissionDay:
                continue
            vSubmissionDayDict[ vSubmissionDay[-1:] ] = vJsonProfile[vSubmissionDay]

        # Getting Current Day
        vToday = datetime.datetime.now()
        # Getting All Future Empty Reports Dates
        vEmptyDays = DohOneGetFutureEmptyReports(DohOneGetFutureReports(vID), ".")

        # Creating An Array with all Week Days for Next 7 Days and Their Respective Date
        vCurrentWeek = dict()
        for i in range(1,8):
            vNextDay = vToday + datetime.timedelta(days = i)
            vNextDayDate = vNextDay.strftime(r"%d.%m.%Y")
            vNextDayNumber = (vNextDay.weekday() + 2) % 7
            if vNextDayNumber == 0:
                vNextDayNumber = 7
            # Adding Day to Array Only if it Needs to by Reported
            if str(vNextDayDate) in vEmptyDays:
                vCurrentWeek[str(vNextDayNumber)] = str(vNextDayDate)

        # Generating DohOne Cookie
        vDohOneCookie = DohOneGenCookie(vID)
        # Looping Through All Empty Days
        for vDayNumber, vDayDate in vCurrentWeek.items():

            # Getting Submission Option For Specified Day
            vDayOption = vSubmissionDayDict[vDayNumber]
            if vDayOption == "":
                continue
            vOptionPrimary = str(vDayOption[:2])
            vOptionSecondary = str(vDayOption[-2:])

            # Adding The Doh Data The Correct Values for Each Day
            vCurrentDohSubmissionData = DOH_SUBMISSION_DATA
            vCurrentDohSubmissionData = vCurrentDohSubmissionData.replace(r"{--A--}", vOptionPrimary)
            vCurrentDohSubmissionData = vCurrentDohSubmissionData.replace(r"{--B--}", vOptionSecondary)
            vCurrentDohSubmissionData = vCurrentDohSubmissionData.replace(r"{--C--}", vDayDate)
            # Sending Doh One Data
            try:
                vSendDohOne = req.post(URL_ATTENDANCE_INSERT, headers={"Host": URL_HOST, "Referer": REFERER_SECONDARIES,"User-Agent": USER_AGENT, "Content-Type": CONTENT_TYPE_MULTIPART}, cookies={"AppCookie": vDohOneCookie}, data=vCurrentDohSubmissionData)
            except:
                continue

        # Finished Function Successfully
        return True
    
    # Everything Fails and Falls Apart
    except:
        return False

# Retrieve DohOne Future Reported Data
# Usage: DohOneGetFutureReports(123456789)
# Returns:
# vDohOneFutureDays     => Returns DohOne (Submitted Only) Futute Reports as an Array
# False                 => if Didnt Retrieve Future Reports
# Parameters:
# vID                   => the Profile ID Number
def DohOneGetFutureReports(vID):
    # Converting Parameters to Correct Type
    vID = str(vID)
    
    try:
        # Get DohOne Cookie and Current Month and Year in Json Format
        vDohOneCookie = DohOneGenCookie(vID)
        vToday = datetime.datetime.now()
        DATE_DATA = '{"month":' + str(vToday.month) + \
            ',"year":' + str(vToday.year) + '}'

        # Request all Future Days and Their Submitted Options
        vDohOneFutureDays = req.post(URL_ATTENDANCE_GET, headers={
            "Host": URL_HOST, "Referer": REFERER_CALENDAR, "User-Agent": USER_AGENT, "Content-Type": CONTENT_TYPE_APPLICATION}, cookies={"AppCookie": vDohOneCookie}, data=DATE_DATA)
        vDohOneFutureDays = str(vDohOneFutureDays.content.decode())
        vDohOneFutureDays = (json.loads(vDohOneFutureDays))['days']
        return vDohOneFutureDays
    
    # Getting Future Reports Failed
    except:
        return False

# Retrieve DohOne Future Non Reported Days, Days Without Submission
# Usage: DohOneGetFutureEmptyReports( DohOneGetFutureReports(123456789), "-" )
# Returns:
# vEmptyDays                    => Returns DohOne Empty (Non Submitted) Days for the Next 7 Days
# False                         => if Shahar changes what their APIs Return and parsing Fails
# Parameters:
# vDohOneFutureDays             => All Reportd Future Days for the Next 7 Days, Returned From the DohOneGetFutureReports() Function
# vDohOneFutureDaysDelimiter    => Delimiter for The Date, Default: '-'
def DohOneGetFutureEmptyReports(vDohOneFutureDays, vDohOneFutureDaysDelimiter = "-"):
    try:
        # Creating a list of all days from Tommorow to Sam Day Next Week (Today + 7)
        vToday = datetime.datetime.now()
        vCurrentWeek = list()
        for vNextDay in range(1,8):
            vDayOfWeek = vToday + datetime.timedelta(days = vNextDay)
            vDayOfWeek = vDayOfWeek.strftime(r"%d-%m-%Y")
            vCurrentWeek.append(vDayOfWeek)

        # Creating a list of all Days With Reported Data
        vReportedDays = list()
        for vFutureDay in vDohOneFutureDays:
            vFutureDayDate = vFutureDay['date'][:REMOVE_SECONDS_FROM_DATE]
            vFutureDayDate = datetime.datetime.strptime(vFutureDayDate, r"%Y-%m-%d")
            vFutureDayDate = str(vFutureDayDate.strftime(r"%d-%m-%Y"))
            vReportedDays.append(vFutureDayDate)

        # Comparing The Two Lists
        vEmptyDays = list()
        for vDayOfWeek in vCurrentWeek:
            if vDayOfWeek not in vReportedDays:
                # Replace "-" With Choosen Delimiter
                vEmptyDays.append(vDayOfWeek.replace("-",vDohOneFutureDaysDelimiter))
        return vEmptyDays
    except:
        return False

# --------------------------------------------------------- #

# DohOne SubmissionOptions Functions

# Retrieve the Submission Options for the Specified Profile
# Usage: DohOneGetSubmissionOptions([DohOne Cookie]) 
# Returns:
# vDohOneSubmissionOptions  => Returns The Submission Options For DohOne
# False                     => if Failed to Request one.prat.idf.il
# Parameters:
# vDohOneCookie             => the DohOne Cookie generated by DohOneGenCookie()
def DohOneGetSubmissionOptions(vDohOneCookie):
    try:
        vDohOneSubmissionOptions = req.get(URL_ATTENDANCE_OPTIONS, headers={"Host": URL_HOST, "Referer": REFERER_HP,"User-Agent": USER_AGENT}, cookies={"AppCookie": vDohOneCookie})
        vDohOneSubmissionOptions = dict(json.loads(vDohOneSubmissionOptions.content))
        return vDohOneSubmissionOptions['primaries']
    except:
        return False

# Format the Output of the DohOneGetSubmissionOptions() Function and Print all Options
# Usage: DohOneFormatSubmissionOptions( DohOneGetSubmissionOptions([DohOne Cookie]) )
# Returns:
# {vPrimaryOptionCode}-{vSecondaryOptionCode}   => Returns The Choosen Option Codes for Submission Seperated by "-"
# False                                         => if Failed Somehoe to Parse The Text
# Parameters:
# vDohOneSubmissionOptions                      => the DohOne Submission Options generated by DohOneGetSubmissionOptions()
def DohOneFormatSubmissionOptions(vDohOneSubmissionOptions):
    try:
        # Print All Primary Options
        for vPrimaryOption in vDohOneSubmissionOptions:
            print(fr"{vPrimaryOption['statusCode']} - {vPrimaryOption['statusDescription'][::REVERSE_STRING_FOR_HEBREW]}")
        # Ask User For Wanted Primary Option To Auto Send
        vPrimaryOptionCode = input("Select Primary Option Number => ")

        # Print All Secondary Options for the Selected Primary Option
        for vPrimaryOption in vDohOneSubmissionOptions:
            if vPrimaryOption['statusCode'] != vPrimaryOptionCode:
                continue
            for vSecondaryOption in vPrimaryOption['secondaries']:
                print(fr"{vSecondaryOption['statusCode']} - {vSecondaryOption['statusDescription'][::REVERSE_STRING_FOR_HEBREW]}")
        # Ask User For Wanted Secondary Option To Auto Send
        vSecondaryOptionCode = input("Select Secondary Option Number => ")

        return fr"{vPrimaryOptionCode}-{vSecondaryOptionCode}"
    
    # Function Fails Somehow, although its just parsing text
    except:
        return False

# Get The Default Submission for each Day
# Usage: DohOneGetDefaultSubmissionOption(123456789, 7)
# Returns:
# SubmissionOption of DayNumber => Returns The SubmissionOption of the Specified Day Of Week
# False                         => if Failed to Get Profile Data
# Parameters:
# vID                           => the Profile ID Number
# vDayNumber                    => Day Of Week, e.g: 1 = Sunday, 2 = Monday, 7 = Saturday
def DohOneGetDefaultSubmissionOption(vID, vDayNumber):
    # Converting Parameters to Correct Type
    vID = str(vID); vDayNumber = str(vDayNumber)

    try:
        # Retrieving SubmissionOption For The Specified vID and Day of Week
        vProfile = JsonGetProfile(vID)
        return vProfile[fr"{JSON_DATABASE_SUBMISSION_NAME}{vDayNumber}"]
    except:
        return False

# Set The Default Submission for each Day
# Usage: DohOneSetDefaultSubmissionOption(123456789, 1, ("01-02" or DohOneFormatSubmissionOptions()))
# Returns:
# True                  => if Function Succeeded and Default Submission Option Changed
# False                 => if Function Failed and Default Submission Option Didnt Changed
# Parameters:
# vID                   => the Profile ID Number
# vDayNumber            => Day Of Week, e.g: 1 = Sunday, 2 = Monday, 7 = Saturday
# vSubmissionOption     => The Submission Option, e.g: 01-02 or 02-05
def DohOneSetDefaultSubmissionOption(vID, vDayNumber, vSubmissionOption):
    # Converting Parameters to Correct Type
    vID = str(vID); vDayNumber = str(vDayNumber); vSubmissionOption = str(vSubmissionOption)

    try:
        # Setting the SubmissionOption For The Specified vID and Day of Week
        JsonSetProfile(vID, fr"{JSON_DATABASE_SUBMISSION_NAME}{vDayNumber}", vSubmissionOption)
        return True
    
    # If Function Fails
    except:
        return False

# --------------------------------------------------------- #

# Main
def main():

    # Arguments Parser
    vArgumentParser = argparse.ArgumentParser(description="The AutoDohOne Arghuments")
    # Adding Arguments
    vArgumentParser.add_argument("--ID", type=str, help="Specify The User ID")
    vArgumentParser.add_argument("--Pass", type=str, help="Specify The User Password")
    vArgumentParser.add_argument("--Name", type=str, help="Specify The User Real Name")
    vArgumentParser.add_argument("--AuthKey", type=str, help="Specify The User AuthKey")
    vArgumentParser.add_argument("--ProfileKey", type=str, help="Specify The Profile Key To Change")
    vArgumentParser.add_argument("--ProfileValue", type=str, help="Specify The Profile Value To Change")
    vArgumentParser.add_argument("--Force", action="store_true", help="Setting Force Mode For Functions")

    # Adding Token Functions
    vArgumentParser.add_argument("--GenerateAuthToken",action="store_true", help=f"{TEXT_COLOR_BLUE}[Requires: ID, Pass | Optional: --SetAuthToken]{TEXT_COLOR_RESET} Generate New AuthToken for The Specified ID and Password")
    vArgumentParser.add_argument("--ShowAuthToken", action="store_true", help=f"{TEXT_COLOR_BLUE}[Requires: ID]{TEXT_COLOR_RESET} Retrieve AuthToken for The Specified ID")
    vArgumentParser.add_argument("--SetAuthToken",action="store_true", help=f"{TEXT_COLOR_BLUE}[Requires: ID, AuthKey]{TEXT_COLOR_RESET} Sets Given AuthKey for The Specified ID,\nCan Be Coupled Together with --GenerateAuthToken instead of Directly Giving AuthKey, in order to Generate New Key and Set in Database Automatically")

    # Adding Profile Functions
    vArgumentParser.add_argument("--CreateDatabase",action="store_true", help=f"{TEXT_COLOR_BLUE}[Optional: Force]{TEXT_COLOR_RESET} Create a New Json Profile Database, When Used With --Force it Overrides the Current Database")
    vArgumentParser.add_argument("--CheckDatabase",action="store_true", help=f"Checks if Database Exists")
    vArgumentParser.add_argument("--NewProfile",action="store_true", help=f"{TEXT_COLOR_BLUE}[Requires: ID, Name]{TEXT_COLOR_RESET} Creates a New Profile")
    vArgumentParser.add_argument("--DeleteProfile",action="store_true", help=f"{TEXT_COLOR_BLUE}[Requires: ID]{TEXT_COLOR_RESET} Deletes Existing Profile")
    vArgumentParser.add_argument("--GetProfile",action="store_true", help=f"{TEXT_COLOR_BLUE}[Requires: ID]{TEXT_COLOR_RESET} Get Profile Information")
    vArgumentParser.add_argument("--SetProfile",action="store_true", help=f"{TEXT_COLOR_BLUE}[Requires: ID, ProfileKey, ProfileValue]{TEXT_COLOR_RESET} Change Profile Information")

    # Adding DohOne Functions
    vArgumentParser.add_argument("--SendDohOne",action="store_true", help=f"{TEXT_COLOR_BLUE}[Requires: ID]{TEXT_COLOR_RESET} Send DohOne Report for Specified ID, or all Profiles if --ID is '*',\n Reports Only Empty Days and only According to Profile Settings")
    vArgumentParser.add_argument("--GenDohOneCookie",action="store_true", help=f"{TEXT_COLOR_BLUE}[Requires: ID]{TEXT_COLOR_RESET} Generate DohOne Cookie for Specified ID")
    vArgumentParser.add_argument("--GetDohOneCurrentOptions",action="store_true", help=f"{TEXT_COLOR_BLUE}[Requires: ID]{TEXT_COLOR_RESET} Get Current DohOne Report Setting for Specified ID")
    vArgumentParser.add_argument("--GetDohOneAvailableOptions",action="store_true", help=f"{TEXT_COLOR_BLUE}[Requires: ID]{TEXT_COLOR_RESET} Get Available DohOne Report Options from the Website")
    vArgumentParser.add_argument("--SetDohOneOptions",action="store_true", help=f"{TEXT_COLOR_BLUE}[Requires: ID, ProfileKey, ProfileValue]{TEXT_COLOR_RESET} Set Default DohOne Report Settings for Specified ID,\nProfileKey is the Day Number\nProfileValue is The Report Code Acquired from using --GetDohOneAvailableOptions")
    

    #vArgumentParser.add_argument("--GetDohOneReport",action="store_true", help=f"{TEXT_COLOR_BLUE}[Requires: ID] Retrieve DohOne Reprted Data from Log")
    #vArgumentParser.add_argument("--LogDohOneReport",action="store_true", help=f"Retrieve DohOne Reprted Data for Logging Purposes")
    # Finishing Argument Parsing
    vArgs = vArgumentParser.parse_args()

    # ---------------------------------- #

    # Start Main Script Functionality

    # ---------------------------------- #

    # Token Functions

    if vArgs.GenerateAuthToken:
        MicrosoftGenAuthKey()

    if vArgs.ShowAuthToken:
        # Check Dependencies
        if not vArgs.ID:
            print(f"{TEXT_COLOR_RED}Missing ID{TEXT_COLOR_RESET}")
            exit()
        # Retrieving Auth Key
        vAuthKey = MicrosoftGetAuthKey(vArgs.ID)
        if vAuthKey:
            print(fr"AuthKey: {vAuthKey}")
        else:
            print(fr"{TEXT_COLOR_RED}AuthKey Generation Failed for {vArgs.ID}{TEXT_COLOR_RESET}")
    
    if vArgs.SetAuthToken:
        # Check Dependencies
        if not vArgs.ID or not vArgs.AuthKey:
            print(f"{TEXT_COLOR_RED}Missing ID / AuthKey{TEXT_COLOR_RESET}")
            exit()
        # Setting Authentication Key for Profile
        if (MicrosoftSetAuthKey(vArgs.ID, vArgs.AuthKey)):
            print(fr"{TEXT_COLOR_GREEN}Set AuthKey for {vArgs.ID}{TEXT_COLOR_RESET} Successfully")
        else:
            print(fr"{TEXT_COLOR_RED}Failed Setting AuthKey for {vArgs.ID}{TEXT_COLOR_RESET}")
    
    # ---------------------------------- #

    # Profile Functions
    
    if vArgs.CreateDatabase:
        # Create a New Database
        if (JsonCreateFile(vForce=vArgs.Force)):
            print(f"{TEXT_COLOR_GREEN}Database was Created{TEXT_COLOR_RESET}")
        else:
            print(f"{TEXT_COLOR_RED}Databse was not Created{TEXT_COLOR_RESET}")
    
    if vArgs.CheckDatabase:
        # Check if Database Exists
        if (JsonIsExist()):
            print(f"{TEXT_COLOR_GREEN}Profile Database Exists{TEXT_COLOR_RESET}")
        else:
            print(f"{TEXT_COLOR_RED}Profile Database Missing{TEXT_COLOR_RESET}")
    
    if vArgs.NewProfile:
        # Check Dependencies
        if not vArgs.ID or not vArgs.Name:
            print(f"{TEXT_COLOR_RED}Missing ID / Name{TEXT_COLOR_RESET}")
            exit()
        # Create New Profile
        if (JsonNewProfile(vArgs.ID, vArgs.Name)):
            print(f"{TEXT_COLOR_GREEN}New Profile Created{TEXT_COLOR_RESET}")
        else:
            print(f"{TEXT_COLOR_RED}New Profile Creation Failed{TEXT_COLOR_RESET}")
    
    if vArgs.DeleteProfile:
        # Check Dependencies
        if not vArgs.ID:
            print(f"{TEXT_COLOR_RED}Missing ID{TEXT_COLOR_RESET}")
            exit()
        # Delete Profile
        if (JsonDeleteProfile(vArgs.ID)):
            print(fr"{TEXT_COLOR_GREEN}{vArgs.ID} Profile Deleted{TEXT_COLOR_RESET}")
        else:
            print(fr"{TEXT_COLOR_RED}{vArgs.ID} Profile Deletion Failed{TEXT_COLOR_RESET}")

    if vArgs.GetProfile:
        # Check Dependencies
        if not vArgs.ID:
            print(f"{TEXT_COLOR_RED}Missing ID{TEXT_COLOR_RESET}")
            exit()
        # Retrieve all Profile Information
        vProfile = JsonGetProfile(vArgs.ID)
        if vProfile == False:
            print(fr"{TEXT_COLOR_RED}Getting {vArgs.ID} Profile Failed{TEXT_COLOR_RESET}")
        else:
            print(fr"Profile             : {vArgs.ID}")
            for vKey, vValue in dict(vProfile).items():
                if vKey == JSON_DATABASE_AUTHKEY:
                    print(fr"{JSON_DATABASE_AUTHKEY.ljust(20)}: <Classified>")
                    continue
                print(fr"{vKey.ljust(20)}: {vValue}")
    
    if vArgs.SetProfile:
        # Check Dependencies
        if not vArgs.ID or not vArgs.ProfileKey or not vArgs.ProfileValue:
            print(f"{TEXT_COLOR_RED}Missing ID / ProfileKey / ProfileValue{TEXT_COLOR_RESET}")
            exit()
        # Changing Profile Values
        if (JsonSetProfile(vArgs.ID, vArgs.ProfileKey, vArgs.ProfileValue)):
            print(fr"{TEXT_COLOR_GREEN}Changed {vArgs.ID} {vArgs.ProfileKey} to {vArgs.ProfileValue}{TEXT_COLOR_RESET}")
        else:
            print(fr"{TEXT_COLOR_RED}Failed to Change {vArgs.ID} {vArgs.ProfileKey}{TEXT_COLOR_RESET}")
            
    # ---------------------------------- #
    
    # DohOne Functions
            
    if vArgs.SendDohOne:
        # Check Dependencies
        if not vArgs.ID:
            print(f"{TEXT_COLOR_RED}Missing ID{TEXT_COLOR_RESET}")
            exit()
        # Send DohOne Report for Single User
        if vArgs.ID != "*":
            DohOneSendFutureReport(vArgs.ID)
            exit()
        # Send DohOne Report for all Users
        vAllProfiles = JsonGetAllProfiles()
        for vProfile in vAllProfiles:
            try:
                DohOneSendFutureReport(vProfile)
            except:
                continue

    if vArgs.GenDohOneCookie:
        # Check Dependencies
        if not vArgs.ID:
            print(f"{TEXT_COLOR_RED}Missing ID{TEXT_COLOR_RESET}")
            exit()
        print(f"{vArgs.ID} DohOne Cookie:\n{DohOneGenCookie(vArgs.ID)}")

    if vArgs.GetDohOneCurrentOptions:
        # Check Dependencies
        if not vArgs.ID:
            print(f"{TEXT_COLOR_RED}Missing ID{TEXT_COLOR_RESET}")
            exit()
        # Get All Currect Reporting Options for Selected Profile
        for vDay in range(1,8):
            print(fr"Day {vDay}: {DohOneGetDefaultSubmissionOption(vArgs.ID, vDay)}")
    
    if vArgs.GetDohOneAvailableOptions:
        # Check Dependencies
        if not vArgs.ID:
            print(f"{TEXT_COLOR_RED}Missing ID{TEXT_COLOR_RESET}")
            exit()
        # Get All Available Report Options From DohOne Website
        DohOneFormatSubmissionOptions(DohOneGetSubmissionOptions(DohOneGenCookie(vArgs.ID)))

    if vArgs.SetDohOneOptions:
        if not vArgs.ID or not vArgs.ProfileKey or not vArgs.ProfileValue:
            print(f"{TEXT_COLOR_RED}Missing ID / ProfileKey / ProfileValue{TEXT_COLOR_RESET}")
            exit()
        if (JsonSetProfile(vArgs.ID, vArgs.ProfileKey, vArgs.ProfileValue, vChangingDays = True)):
            print(fr"{TEXT_COLOR_GREEN}Successfully Set {vArgs.ID} Option for Day {vArgs.ProfileKey} to {vArgs.ProfileValue}{TEXT_COLOR_RESET}")
        else:
            print(fr"{TEXT_COLOR_RED}Failed Setting {vArgs.ID} Option for Day {vArgs.ProfileKey} to {vArgs.ProfileValue}{TEXT_COLOR_RESET}")

# Calling Main
if __name__ == "__main__":
    main()
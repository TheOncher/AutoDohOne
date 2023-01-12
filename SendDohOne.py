# Imports
import requests as req
import datetime
import time
import json
import os

# Constants
URL_LOGIN = r"https://one.prat.idf.il/api/account/login"
URL_ATTENDANCE_INSERT = r"https://one.prat.idf.il/api/Attendance/InsertFutureReport"
URL_ATTENDANCE_GET = r"https://one.prat.idf.il/api/Attendance/getFutureReport"
HOST = r"one.prat.idf.il"
REFERER_LOGIN = r"https://one.prat.idf.il/login"
REFERER_SECONDARIES = r"https://one.prat.idf.il/secondaries"
REFERER_CALENDAR = r"https://one.prat.idf.il/calendar"
USER_AGENT = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"
CONTENT_TYPE_MULTIPART = r"multipart/form-data; boundary=----WebKitFormBoundaryYYzAwUiDj80Dh1q1"
CONTENT_TYPE_APPLICATION = r"application/json;charset=UTF-8"
DOH_DATA = "\r\n------WebKitFormBoundaryYYzAwUiDj80Dh1q1\r\nContent-Disposition: form-data; name=\"MainCode\"\r\n\r\n01\r\n------WebKitFormBoundaryYYzAwUiDj80Dh1q1\r\nContent-Disposition: form-data; name=\"SecondaryCode\"\r\n\r\n01\r\n------WebKitFormBoundaryYYzAwUiDj80Dh1q1\r\nContent-Disposition: form-data; name=\"Note\"\r\n\r\n\r\n------WebKitFormBoundaryYYzAwUiDj80Dh1q1\r\nContent-Disposition: form-data; name=\"FutureReportDate\"\r\n\r\n{---}\r\n------WebKitFormBoundaryYYzAwUiDj80Dh1q1--\r\n"
# AUTH_KEY = "INSERT YOUR AUTH KEY HERE"
# Used for Repl.it, can be ignored
# AUTH_KEY = os.environ['AUTH_TOKEN']


def RequestAppCookie(AUTH_KEY):
    RequestAppCookie = req.get(URL_LOGIN, headers={"Authorization": AUTH_KEY,
                                                   "Host": HOST, "Referer": REFERER_LOGIN, "User-Agent": USER_AGENT})
    for cookie in RequestAppCookie.cookies:
        if "Cookie AppCookie=" in str(cookie):
            AppCookieRaw = cookie
            AppCookie = str(cookie).split(" ")[1]
            AppCookieData = (str(cookie).split(" ")[1]).split("=")[1]
    return AppCookieData


def SendDohOne(AppCookieData, Date):
    SendDohOne = req.post(URL_ATTENDANCE_INSERT, headers={"Host": HOST, "Referer": REFERER_SECONDARIES,
                                                          "User-Agent": USER_AGENT, "Content-Type": CONTENT_TYPE_MULTIPART}, cookies={"AppCookie": AppCookieData}, data=DOH_DATA.replace(r"{---}", str(Date)))
    return SendDohOne


def GetEmptyDays(AppCookieData):
    Today = datetime.datetime.now()
    TodayWeekDayNumber = int(Today.date().strftime("%w")) + 1
    DATE_DATA = '{"month":' + str(Today.month) + \
        ',"year":' + str(Today.year) + '}'

    GetEmptyDays = req.post(URL_ATTENDANCE_GET, headers={
        "Host": HOST, "Referer": REFERER_CALENDAR, "User-Agent": USER_AGENT, "Content-Type": CONTENT_TYPE_APPLICATION}, cookies={"AppCookie": AppCookieData}, data=DATE_DATA)

    EmptyDays = GetEmptyDays.content.decode()
    EmptyDays = (EmptyDays.split("[")[1]).split("]")[0]
    EmptyDays = (EmptyDays[1:-1]).split("},{")
    ReportedDays = ''
    for Line in EmptyDays:
        Line = Line.split(r",")[2]
        Line = (Line.split(":")[1])[1:-3]
        Line = Line.split("-")
        LineYear = int(Line[0])
        LineMonth = int(Line[1])
        LineDay = int(Line[2])
        ReportedDays += str(int(datetime.date(LineYear,
                            LineMonth, LineDay).strftime("%w"))+1)
        ReportedDays += ","

    AllWeekNumbers = ['1', '2', '3', '4', '5']
    for day in ReportedDays.split(r","):
        if day in AllWeekNumbers:
            AllWeekNumbers.remove(day)

    EmptyDates = list()
    for day in AllWeekNumbers:
        day = int(day)
        if TodayWeekDayNumber >= day:
            day += 7
        DayDifference = day - TodayWeekDayNumber
        EmptyDates.append(Today + datetime.timedelta(days=DayDifference))
    return EmptyDates


def main():
    while (True):
        AppCookieData = RequestAppCookie(AUTH_KEY)
        EmptyDays = GetEmptyDays(AppCookieData)
        for Day in EmptyDays:
            Day = Day.strftime(r"%d.%m.%Y")
            DohOne = SendDohOne(AppCookieData, str(Day))
            print(f"{DohOne.status_code} at {str(datetime.datetime.now())}")
        time.sleep(86400)


if __name__ == "__main__":
    main()

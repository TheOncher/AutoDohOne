# Important #
The IDF only accept API requests and any other form of access to its sites from israeli IP's
Besure to ONLY use cloud servers based in israel, Oracle have servers in jerusalem.
The best practice is to use Oracle Cloud, open up an account and deploy an always free linux VM instance,
Remember, Oracle Cloud Always Free VM's are ALWAYS FREE and the entire deployment of this Automation should never cost a penny.
Follow their guides to set up a budget of 1 dollar just to be sure, either way, safe practice is best practice.

# Persistency #
This is a script to help you automated the irritating task of remembering to fill DohOne everyday.
Upload SendDohOneLinuxDeployment.py to your linux machine and add an appropriate cron tab
to fully automate the execution of the script without locking the terminal up.
Download Base SendDohOne.py to run in your windows computer or server inside a "while True" loop.
The best practice is to upload SendDohOneLinuxDeployment.py to the cloud so to have persistency and
confidence in the succsesfull execution of the script without worry of poweroutage or restart.

# Acquiring AUTH_TOKEN #
Basic Preknowledge in BurpSuite is required
Start BurpSuite in your browser, activate proxy to forward all data to burp, and add "https://one.prat.idf.il/" to the target scope for best practice,
Start intercepting the requests, authenticate to the site "https://one.prat.idf.il/login" normally via the Microsoft Azure Authentication
implemented by the IDF, and keep forwarding the requests manually until you see a "GET /api/account/login HTTP/2" with " Authorization: "
data inside the request, it should be under the request headers.
This " Authorization " request should be the second one but check all of them any way to besure.
Remember to get a new AUTH_TOKEN every 60 days MAX! preferably less than that.

# The Script #
This python script uses the IDF API's to send doh one automatically, you can loop it or make a scheduled task that will run it for you.
It will look at all the empty days you didn't fill yourself and fill them for you with "Present At Base", the default choise for most people.
The script will not override a manual submit, so if you take a vacation or want to fill something different than "Present",
just change the doh yourself normally via the app or website for the specified day.
The script will not run over a manual submit, but it will refill an empty sumbit, so if you delete one, the next time the script executes,
it will fill it with "Present At Base" or anything else you set it up with.

TL:DR - The script auto fills with "Present" for the whole week, and will not run over a manual submit if you choose to take a vacation,
It will refill a day if you delete one and leave it empty.

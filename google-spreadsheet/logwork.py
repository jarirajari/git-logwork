import sys, re, datetime
from apiclient import discovery
from apiclient.errors import HttpError
import google.auth
from google.oauth2 import service_account
from google.auth.transport.urllib3 import AuthorizedHttp

ERROR = "-"
SUCCESS = "+"

def addNewWorkHoursItem(work, issue, date, keyfile, spreadid, sheetname, a1range):
	TYPE="sheets"
	VERSION = "v4"
	SCOPE="https://www.googleapis.com/auth/spreadsheets"
	TOKEN = keyfile
	SID = spreadid
	success = False

	credentials = service_account.Credentials.from_service_account_file(TOKEN)
	scoped_credentials = credentials.with_scopes([SCOPE])
	service = discovery.build(TYPE, VERSION, credentials=scoped_credentials)
	try:
		values = [[str(datetime.datetime.now()), work, issue, date]]
		response = service.spreadsheets().values().append(spreadsheetId=SID, range=(str(sheetname)+"!"+a1range), valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={'values': values}).execute()
		# trailing 'u' is caused by Python2 unicode handling u'<text>'
		result = SUCCESS
	except HttpError as err:
		# err.resp.status not 200, see reason with 'str(err)'
		result = str(err)
	return result

def checkWork(work):
	parsed = 0
	work = re.sub(r"\s+", "", work, flags=re.UNICODE)
	result = re.search('^(?!$)(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?', work)
	if result is not None:
		parts = result.groups()
		if len(parts) == 3:
			days = 0 if parts[0] is None else int(parts[0])
			hours = 0 if parts[1] is None else int(parts[1])
			mins = 0 if parts[2] is None else int(parts[2])
			parsed = int(days*(8*60)+hours*(1*60)+mins*(1*1))
	return parsed

def checkIssue(issue):
	parsed = ERROR
	issue = re.sub(r"\s+", "", issue, flags=re.UNICODE)
	result = re.search('^([a-zA-Z]+)-([0-9]{1,6})$', issue)
	if result is not None:
		parts = result.groups()
		if len(parts) == 2:
			parsed = str(parts[0]).upper()+"-"+str(parts[1]).upper()
	return parsed

def checkDate(date):
	parsed = date
	try:
        	datetime.datetime.strptime(date, '%Y-%m-%d')
    	except ValueError:
        	parsed = ERROR
	return parsed

def checkExists(param):
	return True if param is not None else False

def logWork(work, issue, date):
	result = str(checkWork(work)) + " " + str(checkIssue(issue)) + " " + str(checkDate(date))
	return result

def loopback(arg1, arg2, arg3):
	return str(arg1)+str(arg2)+str(arg3)
# Contract
# arg 1: work hours
# arg 2: issue identifier
# arg 3: date
# arg 4: Google Spreadsheet key file
# arg 5: Google Spreadsheet sheet id
# arg 6: Sheet name
# arg 7: A1 range

if checkWork(sys.argv[1]) > 0 and checkIssue(sys.argv[2]) is not ERROR and checkDate(sys.argv[3]) is not ERROR and checkExists(sys.argv[4]) and checkExists(sys.argv[5]) and checkExists(sys.argv[6]) and checkExists(sys.argv[7]):
	sys.exit(addNewWorkHoursItem(checkWork(sys.argv[1]), checkIssue(sys.argv[2]), checkDate(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]))
else:
	sys.exit(ERROR)







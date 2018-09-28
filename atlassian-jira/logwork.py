import sys, re, datetime
import urllib3, base64, json

ERROR = "-"
SUCCESS = "+"

def addNewWorkHoursItem(work_raw, issue, date, api, creds):
	JSON='application/json'
	BASIC_AUTH_HEADER = "Basic "+base64.b64encode(creds)
	REST = api + "issue/"+issue+"/worklog"+"?adjustEstimate=leave"
	# POST /rest/api/2/issue/{issueIdOrKey}/worklog
	data = {
		"timeSpent": formatWork(work_raw),
		"comment": "logged with git logwork",
		"started": str(date)+"T12:00:00.000+0000"
		}
	encoded_data = json.dumps(data).encode('utf-8')
	urllib3.disable_warnings()
	http = urllib3.PoolManager()
	r = http.request('POST', REST, body=encoded_data, headers={'Authorization': BASIC_AUTH_HEADER, 'Content-Type': JSON})
	if r.status == 201:
		result=SUCCESS
	else:
		result=ERROR
	return result

def formatWork(work):
	parsed = 0
	work = re.sub(r"\s+", "", work, flags=re.UNICODE)
	result = re.search('^(?!$)(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?', work)
	if result is not None:
		parts = result.groups()
		if len(parts) == 3:
			parsed = parts[0]+"d "+parts[1]+"h "+parts[2]+"m"
	return parsed

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
# arg 4: JIRA server URL
# arg 5: JIRA user credentials

if checkWork(sys.argv[1]) > 0 and checkIssue(sys.argv[2]) is not ERROR and checkDate(sys.argv[3]) is not ERROR and checkExists(sys.argv[4]) and checkExists(sys.argv[5]):
	sys.exit(addNewWorkHoursItem(sys.argv[1], checkIssue(sys.argv[2]), checkDate(sys.argv[3]), sys.argv[4], sys.argv[5]))
else:
	sys.exit(ERROR)







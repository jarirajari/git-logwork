Make sure you have Python2.7+ installed

Install with pip unless installed already:
- google-auth
- urllib3
- google-api-python-client

Do the following:
- Create a spreadsheet and a sheet with a name
- Create service account and token (see: https://github.com/juampynr/google-spreadsheet-reader)
- Share the spreadsheet with the account
- Download token and find out the absolute path
- Run plugin with 'git logwork 1m TEST-1', and it will prompt for missing env vars!
- Export missing and required env vars e.g. the token path

Enjoy easy work hours reporting with Git!

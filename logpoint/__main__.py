from logpoint import *

import argparse
parser = argparse.ArgumentParser(prog="python -m logpoint","Perform a simple search on logpoint")

parser.add_argument("logpoint","ip or domain of the logoint machine")
parser.add_argument("user","user on behalf of which search is be performed")
parser.add_argument("secret_key","secret key that is used to autheticate the user")
parser.add_argument("query","search query")

args = parser.parse_args()
logpoint = Logpoint(args.logpoint, args.user, args.secret_key, args.query)
queryData = logpoint.create_search_query("| chart count() by device_ip")
search = logpoint.get_search_log(queryData)
search_id = search.json()["search_id"]
print(logpoint.get_logs(search_id))

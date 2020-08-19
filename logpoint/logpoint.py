import requests
import json
import enum

class AllowedData(string,Enum):
    user_preference = "user_preference"
    loginpsect = "loginpsect"
    repos = "logpoint_repos"
    devices = "devices"
    livesearches = "livesearches"


class Logpoint:
    def __init__(self, ip, username, secret_key):
        self.ip = ip
        self.username = username
        self.secret_key = secret_key

    def get_logpoint_data(self, data):
        api_path = "https://"+self.ip+"/getalloweddata"
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "type": data }
        response = requests.post(api_path,data=req_data,verify=False)
        return response.json()

    def get_search_log(self, data):
        api_path = "https://"+self.ip+"/getsearchlogs"
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "requestData": json.dumps(data) }
        response = requests.post(api_path, data=req_data, verify=False)
        return response

    def get_logs(self, search_id):
        queryData = {"search_id": search_id}
        all_results = []
        while(True):
            try:
                result = self.get_search_log(queryData)
                all_results.extend(result.json()['rows'])
                if(result.json()["final"]):
                    break
            except Exception as e:
                print(e)
                break
        return all_results

    def create_search_query(self, query, repo=[], time_range="Last 30 days"):
        queryData = {"timeout": 90,
                     "client_name": "gui",
                     "repos": repo,
                     "starts": {},
                     "limit": 50000,
                     "time_range": time_range,
                     "query": query }
        return queryData


    def get_incidents(self,ts_from,ts_to):
        api_path = "https://"+self.ip+"/incidents"
        queryData = { "version": 0.1,
                      "ts_from": ts_from,
                      "ts_to": ts_to}
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "requestData": json.dumps(queryData) }
        response = requests.post(api_path, data=req_data, verify=False)
        return response


    def get_data_from_incidents(self,incident_obj_id,incident_id,date):
        api_path = "https://"+self.ip+"/get_data_from_incidents"
        queryData = { "incident_obj_id": incident_obj_id,
                      "incident_id": incident_id,
                      "date": date}
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "requestData": json.dumps(queryData) }
        response = requests.post(api_path, data=req_data, verify=False)
        return response

    def get_incident_states(self,ts_from,ts_to):
        api_path = "https://"+self.ip+"/incident_states"
        queryData = { "version": 0.1,
                      "ts_from": ts_from,
                      "ts_to": ts_to}
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "requestData": json.dumps(queryData) }
        response = requests.post(api_path, data=req_data, verify=False)
        return response

    def add_incident_comment(self,id,comments):
        api_path = "https://"+self.ip+"/add_incident_comment"
        queryData = { "version": 0.1,
                      "states": [{
                          "_id": id,
                          "comments": comments
                      }] }
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "requestData": json.dumps(queryData) }
        response = requests.post(api_path, data=req_data, verify=False)
        return response

    def resolve_incidents(self,incident_ids):
        api_path = "https://"+self.ip+"/resolve_incident"
        queryData = { "version": 0.1,
                      "incident_ids": incident_ids}
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "requestData": json.dumps(queryData) }
        response = requests.post(api_path, data=req_data, verify=False)
        return response

    def close_incidents(self,incident_ids):
        api_path = "https://"+self.ip+"/close_incident"
        queryData = { "version": 0.1,
                      "incident_ids": incident_ids}
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "requestData": json.dumps(queryData) }
        response = requests.post(api_path, data=req_data, verify=False)
        return response

    def reopen_incidents(self,incident_ids):
        api_path = "https://"+self.ip+"/reopen_incident"
        queryData = { "version": 0.1,
                      "incident_ids": incident_ids}
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "requestData": json.dumps(queryData) }
        response = requests.post(api_path, data=req_data, verify=False)
        return response

     def get_users(self):
        api_path = "https://"+self.ip+"/get_users"
        req_data = {'username': self.username,
                  'secret_key': self.secret_key
                  }
        response = requests.post(api_path, data=req_data, verify=False)
        return response



if __name__ == "__main__":
    logpoint = Logpoint("10.45.9.141","admin","d2845bfc94d9f2f92bb6f92a9edb31ee")
    queryData = logpoint.create_search_query("| chart count() by device_ip")
    search = logpoint.get_search_log(queryData)
    search_id = search.json()["search_id"]
    print(logpoint.get_logs(search_id))

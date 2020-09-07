import requests
import json
from enum import Enum

class AllowedData(str,Enum):
    """
    Different data that we can get from the logpoint api
    """
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
        """
        Get the allowed data from the logpoint
        :param data: data that you want to be fetched
        :type data: AllowedData

        :returns data in json
        """
        api_path = "https://"+self.ip+"/getalloweddata"
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "type": data }
        response = requests.post(api_path,data=req_data,verify=False)
        return response.json()

    def get_search_log(self, data):
        """
        Get the search id
        :param data:
        :type data:

        :returns search id in json
        """
        api_path = "https://"+self.ip+"/getsearchlogs"
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "requestData": json.dumps(data) }
        response = requests.post(api_path, data=req_data, verify=False)
        return response

    def get_logs(self, search_id):
        """
        Get all the logs from the search id
        :param search_id: search id
        :type search_id: str

        :returns logs in json
        """
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
        """
        Get create the search query
        :param query: logpoint search query
        :type query: str
        :param repo: list of repo
        :type repo: list
        :param time_range: time range
        :type time_range: str

        :returns search query in json
        """
        queryData = {"timeout": 90,
                     "client_name": "gui",
                     "repos": repo,
                     "starts": {},
                     "limit": 50000,
                     "time_range": time_range,
                     "query": query }
        return queryData


    def get_incidents(self,ts_from,ts_to):
        """
        Gets triggered incidents
        :param ts_from: timestamp from which triggered incident is to be fetched
        :type ts_from: str
        :param ts_to: timestamp to which triggered incident is to be fetched
        :type ts_to: str

        :returns data in json
        """
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
        """
        Gets the detail data from the incident
        :param incident_obj_id: incident object id
        :type incident_obj_id: str
        :param incident_id: incident id
        :type incident_id: str
        :param date: date
        :type date: str

        :returns data in json
        """
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
        """
        Get the states of incident
        :param ts_from: timestamp from which triggered incident is to be fetched
        :type ts_from: str
        :param ts_to: timestamp to which triggered incident is to be fetched
        :type ts_to: str

        :returns data in json
        """
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
        """
        Add comment to the incident
        :param id: incident id
        :type id: str
        :param comments: comment to be placed
        :type comments: str

        :return response object
        """
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
        """
        Add comment to the incident
        :param id: incident id
        :type id: str
        :param comments: comment to be placed
        :type comments: str
        
        :return response object
        """
        api_path = "https://"+self.ip+"/resolve_incident"
        queryData = { "version": 0.1,
                      "incident_ids": incident_ids}
        req_data = {'username': self.username,
                    'secret_key': self.secret_key,
                    "requestData": json.dumps(queryData) }
        response = requests.post(api_path, data=req_data, verify=False)
        return response
    
    def close_incidents(self,incident_ids):
        """
        closes the incident
        :param incident_ids: incident id
        :type incident_ids: str

        :return response object
        """
        api_path = "https://"+self.ip+"/close_incident"
        queryData = { "version": 0.1,
                      "incident_ids": incident_ids}
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "requestData": json.dumps(queryData) }
        response = requests.post(api_path, data=req_data, verify=False)
        return response

    def reopen_incidents(self,incident_ids):
        """
         Reopens the incident
        :param incident_ids: incident id
        :type incident_ids: str

        :return response object
        """
        api_path = "https://"+self.ip+"/reopen_incident"
        queryData = { "version": 0.1,
                      "incident_ids": incident_ids}
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "requestData": json.dumps(queryData) }
        response = requests.post(api_path, data=req_data, verify=False)
        return response

    def get_users(self):
        """
        Get users of the logpoint
        :return user data in json
        """
        api_path = "https://"+self.ip+"/get_users"
        req_data = {'username': self.username,
                  'secret_key': self.secret_key
                  }
        response = requests.post(api_path, data=req_data, verify=False)
        return response



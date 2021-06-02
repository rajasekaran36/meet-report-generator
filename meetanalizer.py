import re
from meetcsvhandle import MeetCSVHandler
from meetmapping import MeetMapping
import datetime
class MeetAnalizer:
    __csvhandle = None
    __mapping = None
    __meet_dict = {}
    __mapping_dict_list = []
    __session_details = None
    def __init__(self,csv_file_path,credentials_json_file_path,workbook_name):
        self.__csvhandle= MeetCSVHandler(csv_file_path)
        self.__meet_dict = self.__csvhandle.get_student_dict()
        self.__mapping = MeetMapping(credentials_json_file_path,workbook_name)
        self.__mapping_dict_list = self.__mapping.get_mapping_dict_list()
        self.__session_details = self.__csvhandle.get_session_details()
        self.__compute_duration()
    

    def get_session_details(self):
        return self.__session_details
    

    def get_joined(self):
        present = []
        for rec in self.__meet_dict['meet_records']:
            if(rec.get('Arrival time')!=None):
                present.append(rec)
        return present

    def get_not_joined(self):
        absent = []
        for rec in self.__meet_dict['meet_records']:
            if(rec.get('Arrival time')==None):
                absent.append(rec)
        return absent
    

    def __get_duration(self,end,start):
        start = datetime.datetime.strptime(start, '%H:%M')
        end = datetime.datetime.strptime(end, '%H:%M')
        duration = end - start
        duration_in_minitues = int(duration.total_seconds()/60)
        return duration_in_minitues

    def __compute_duration(self):
        for rec in self.__meet_dict['meet_records']:
            duration = -1
            if(rec.get('Arrival time')!=None):
                duration = self.__get_duration(rec.get('Last Seen'),rec.get('Arrival time'))
            rec["Duration"] = duration
    
    def get_meet_dict(self):
        return self.__meet_dict

    def get_mapping_dict(self):
        return self.__mapping_dict
    
    def get_record_by_gmeet_name(self,gmeet_name):
        for meet_record in self.__meet_dict['meet_records']:
                if(meet_record['Names']==gmeet_name):
                    return meet_record
    
    def get_report_dict_list(self,min_duration=0):
        for report in self.__mapping_dict_list:
            #need to check with all index
            report["Joined as"] = None
            report["Arrival time"] = None
            report["Last Seen"] = None
            report["Duration"] = None
            report["Status"] = "AB"
            report["Comment"] = None
            record = self.get_record_by_gmeet_name(report['gmeet_names'][0])
            if(record!=None):
                report["Joined as"] = record["Names"]
                report["Arrival time"] = record["Arrival time"]
                report["Last Seen"] = record["Last Seen"]
                report["Duration"] = record["Duration"]
                if(report["Duration"]>=min_duration):
                    report["Status"] = "P"
                    if(report["Duration"]<=20):
                        report["Comment"] = "Left Early"
        return self.__mapping_dict_list


    def get_new_names_dict_list(self):
        new_records = []
        allnames = []
        for rec in self.__mapping_dict_list:
            for name in rec['gmeet_names']:
                allnames.append(name)
        
        #print(allnames)
        for meet_record in self.__meet_dict['meet_records']:
            #print(meet_record)
            if(meet_record["Names"] not in allnames):
                #print(meet_record["Names"])
                new_records.append(meet_record)

        #print(new_records)
        return new_records





from meetanalizer import MeetAnalizer
class MeetReport:
    __meet_analizer = None
    __report_dict_list = None
    __class_details = []
    __session_details = None
    def __init__(self,csv_file_path,credentials_json_file_path,workbook_name):
        self.__meet_analizer = MeetAnalizer(csv_file_path,credentials_json_file_path,workbook_name)
        self.__report_dict_list = self.__meet_analizer.get_report_dict_list()
        self.__session_details = self.__meet_analizer.get_session_details()

        
    def get_session_details(self):
        return self.__session_details

    def get_present_rec(self):
        present_dict = []
        for rec in self.__report_dict_list:
            if(rec["Status"] == "P"):
                present_dict.append(rec)
        return present_dict
    
    def get_absent_rec(self):
        absent_dict = []
        for rec in self.__report_dict_list:
            if(rec["Status"] == "AB"):
                absent_dict.append(rec)
        return absent_dict
        
    def get_report_dict_list(self):
        return self.__report_dict_list
    
    def get_new_names_dict_list(self):
        return self.__meet_analizer.get_new_names_dict_list()
    
    def toCSVFile(self,filename):
        with open("reports/"+filename+".csv",'w') as des:
            data_to_write = ",".join(self.__report_dict_list[0].keys()) +'\n'
            for rec_dict in self.__report_dict_list:
                line = ""
                for key in rec_dict:
                    line = line + str(rec_dict[key]) + ","
                data_to_write = data_to_write + line + '\n'
            des.write(data_to_write)

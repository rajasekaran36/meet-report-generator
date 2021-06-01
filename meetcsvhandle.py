import csv
class MeetCSVHandler:
    __file_path = None
    __sheet = []
    __student_dict = {}
    def __init__(self,file_path):
        self.__file_path = file_path
        with open(self.__file_path,'r',encoding="utf8", errors='ignore') as source:
            reader = csv.reader(source,delimiter=",")
            for row in reader:
                self.__sheet.append(row)
        
        self.__sheet = self.clean_up()
        self.prepare_dict()
    
    def clean_up(self):
        c_sheet = []
        for row in self.__sheet:
            c_row = []
            for cell in row:
                c_row.append(cell.replace('"','',cell.count('"')).strip())
            c_sheet.append(c_row)
        return c_sheet

    
    def get_sheet(self):
        return self.__sheet
    
    def get_class_name(self):
        return str(self.__sheet[0][1])
    
    def get_date(self):
        return self.__sheet[1][1]
    
    def get_time(self):
        return self.__sheet[1][3]
    
    def get_meet_id(self):
        return self.__sheet[1][5]

    def get_stuent_details(self):
        return self.__sheet[4:len(self.__sheet)-4]
    
    def get_student_details_dict_list(self):
        list_details = []
        for row in self.get_stuent_details():
            details = {}.fromkeys(self.__sheet[3])
            keys = list(details.keys())
            try:
                for i in range(len(keys)):
                    if(row[i]==''):
                        details[keys[i]] = None
                    else:
                        details[keys[i]] = row[i]
            except IndexError:
                pass
            
            list_details.append(details)
        
        return list_details

    def prepare_dict(self):
        self.__student_dict['class_name'] = self.get_class_name()
        self.__student_dict['date'] = self.get_date()
        self.__student_dict['time'] = self.get_time()
        self.__student_dict['meet_id'] = self.get_meet_id()
        self.__student_dict['meet_records'] = self.get_student_details_dict_list()

    def get_student_dict(self):
        return self.__student_dict
        
    def get_session_details(self):
        return {
            'class_name':self.get_class_name(),
            'date':self.get_date(),
            'start_time':self.get_time(),
            'meet_id':self.get_meet_id(),
        }
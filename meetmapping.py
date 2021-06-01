import gspread

class MeetMapping:
    __mapping_sheet = None
    __mapping_dict_list = []
    def __init__(self,credentials_json_file_path,workbook_name):
        gc = gspread.service_account(filename=credentials_json_file_path)
        wb = gc.open(workbook_name)
        ws = wb.get_worksheet(0)
        self.__mapping_sheet = ws.get_all_values()
        self.__gen_mapping_dict()

    def __gen_mapping_dict(self):
        for rec in self.__mapping_sheet:
            self.__mapping_dict_list.append({
                "id":rec[0],
                "roll_no":rec[1],
                "name":rec[2],
                "gmeet_names":list(rec[3:])
            });
    
    def get_mapping_dict_list(self):
        return self.__mapping_dict_list

    def get_mapping_sheet(self):
        return self.__mapping_sheet

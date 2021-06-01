from meetreport import MeetReport 
meet_report = MeetReport('resources/data.csv','resources/credentials.json','atn-mapping')
for el in meet_report.get_report_dict_list():print(el)
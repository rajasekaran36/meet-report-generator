from re import template
from flask import Flask,jsonify,request
from flask.templating import render_template
from werkzeug.utils import send_file
from flask_cors import CORS
from meetreport import MeetReport
import datetime
import os

app = Flask(__name__)
CORS(app)

#globals
filename = ""
meet_report = ""


app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'meet_files')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit',methods=["POST"])
def handle():
    #get time stamp as filename begin
    global filename,meet_report
    time_stamp = str(datetime.datetime.now())
    time_stamp = time_stamp.replace(":",'-',time_stamp.count(':'))
    time_stamp = time_stamp.replace(" ",'_',time_stamp.count(' '))
    
    submitted_file = request.files['file']
    filename = time_stamp+"_"+submitted_file.filename
    #stored at meet_files
    submitted_file.save("meetfiles/"+filename)
    meet_report = MeetReport("meetfiles/"+filename,'resources/credentials.json','atn-mapping')
    key_list = list(meet_report.get_report_dict_list()[0].keys())
    key_list = [key.upper() for key in key_list]    
    session_list = [key.upper() for key in meet_report.get_session_details().keys()]
    print(meet_report.get_session_details())
    return render_template("report.html",headings=key_list, reports=meet_report.get_report_dict_list(),session_headings=session_list,session_details=meet_report.get_session_details(),new_rec=meet_report.get_new_names_dict_list())

@app.route('/file')
def file():
    global filename
    return filename

@app.route('/reporthtml')
def reporthtml():
    meet_report = MeetReport('resources/data.csv','resources/credentials.json','atn-mapping')
    key_list = list(meet_report.get_report_dict_list()[0].keys())
    key_list = [key.upper() for key in key_list]    
    session_list = [key.upper() for key in meet_report.get_session_details().keys()]
    #print(meet_report.get_session_details())
    print(meet_report.get_new_names_dict_list())
    return render_template("report.html",headings=key_list, reports=meet_report.get_report_dict_list(),session_headings=session_list,session_details=meet_report.get_session_details(),new_rec=meet_report.get_new_names_dict_list())


if __name__ == "__main__":
    app.run(debug=True)
    
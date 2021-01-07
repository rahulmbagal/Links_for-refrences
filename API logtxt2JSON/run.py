# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 13:38:07 2020

@author: rahul
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 15:19:49 2020

@author: rahul
"""

import os

from json_convert import LogJsonConvertor

from flask import json, current_app


from flask import Flask, request, Response
import numpy as np
import pandas as pd
import flasgger
from flasgger import Swagger
from flask import jsonify
#import json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask import make_response

import os      # For File Manipulations like get paths, rename
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import sys

app=Flask(__name__)
Swagger(app)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


from werkzeug.exceptions import default_exceptions

@app.route('/json_convert_Sucess_logs',methods=["POST"])
def only_Success_LogToJson():
    """Log txt file to JSON API : with successful log cycles only
    Captures all the successful log cycles 
    input only text log file.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
      
    responses:
        200:
            description: The output values
        500:
            description: Error
    
        
    """
    log_json = LogJsonConvertor()


    
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(filename)

    try:
        file_loading = log_json.load_file(filename)
        if (file_loading == -1):
            raise ValueError("Incorrect file extension!")
    except ValueError as ve:
        return str(ve)
                
    extract_val = log_json.extract_values_from_log(file_loading)
    final_2 = log_json.convert_df_to_json(extract_val)
    
    return final_2

@app.route('/json_convert_',methods=["POST"])
def basicLogToJson():
    """Basic Log txt file to JSON API
    log to JSON format API : convert all the relavent lines 
    input only text log file.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
      
    responses:
        200:
            description: The output values
        500:
            description: Error        
    """
    log_json = LogJsonConvertor()
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(filename)
    
    print ("filename +++++=== ", filename)
    
    try:
        file_loading = log_json.load_file(filename)
        print ("file_loading +++++=== ", file_loading)
        if (file_loading == -1):
            raise ValueError("Incorrect file extension!")
    except ValueError as ve:
        return str(ve)
    print ("file_loading === ", file_loading)    
    extract_val = log_json.extract_values_from_log(file_loading)
    print ("extract_val === ", extract_val)
    final_1 = log_json.basic_convert_df_to_json(extract_val)
    
    return final_1



if __name__=='__main__':
#    app.run(port=80, threaded=True, debug=False, host='0.0.0.0')

#    app.debug = True
    # app.run(threaded=True)
      app.run(host='0.0.0.0', threaded=True)
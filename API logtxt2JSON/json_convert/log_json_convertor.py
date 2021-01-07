#loading packages
import re
from pandas import DataFrame
import numpy as np
import os
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class LogJsonConvertor:

    #load txt log_file
    def load_file(self, filepath):
        temp = []
        try:
            ext = os.path.splitext(filepath)[-1].lower()
            if ext == ".txt":
                try:
                    with open(filepath) as fp:
                        for cnt, line in enumerate(fp):
                            temp.append([cnt, line])
                    for i in range(len(temp)):
                        temp[i][1] = str(temp[i][1]).strip('\n')
                except IOError as e:
                    print(e)
#                 finally:
#                     print("exit")    
            else:
                raise ValueError("Incorrect file extension!")
        except ValueError as ve:
            return -1
        return temp    

    # function to extracting values from the each line of the text
    def extract_values_from_text(self, string_temp_, pattern_search):
        string_temp = str(string_temp_[1])
        match = re.search(pattern_search, str(string_temp))  
        if match != None:
            #############################################
            #extract the position and the string of "operation"
            match = re.search(pattern_search, str(string_temp))  
            operation = string_temp[match.start():match.end()-1]
            
            if operation == "ENTER":
                operation = str("ENTRY")
            #############################################
            #extract the position and the string of "filename"
            file_name_temp = str(string_temp[match.end():])
            index_colon = re.search(":", str(file_name_temp))  
            filename = str(file_name_temp[:index_colon.start()]).strip()

            #############################################
            #extract the position and the string of "line_number"
            line_number_temp_1 =  str(file_name_temp[index_colon.end():])
            line_number_temp_2 = re.search(r'\d+', line_number_temp_1) 
            line_number = line_number_temp_1[line_number_temp_2.start():line_number_temp_2.end()]
            #############################################
            #extract the position and the string of "name"
            # name follows the following rule: must begin with (unicode_letter or _), and can end with many (unicode_letter, unicode_digit or _).
            try:
                name_temp = str(line_number_temp_1[line_number_temp_2.end():]).lstrip()
    #             if len(name_temp)<1:
    #                 name = "None"
    #             else:
                if ((name_temp[0].isalpha()) or (name_temp[0] == "_")) and (name_temp[len(name_temp)-1].isalpha() or (name_temp[len(name_temp)-1] == "_") or name_temp[len(name_temp)-1].isdigit()):
                    name = str(name_temp).rstrip()
                elif name_temp == "0":
                    name = "anonymous"
                else: 
                    name = "invalid input"
            except IndexError:
                name = "invalid input"

            return [string_temp_[0], string_temp, operation, filename, line_number, name]    

    # function iterates each line of the txt and call the "extract_values_from_text" , the output is the pandas dataframe 
    def extract_values_from_log(self, temp):
        list_all = []
        lists = ["Line no.", "text", "operation", "filename", "line_number", "name"]

        for i in range(0,len(temp)):
            string_t = temp[i]
            if  (re.search(str("ENTER:"), string_t[1])) !=None:
                list_all.append(self.extract_values_from_text(string_t, str("ENTER:")))
            elif (re.search(str("EXIT:"), string_t[1])) !=None:
                list_all.append(self.extract_values_from_text(string_t, str("EXIT:")))
            else:
                list_all.append([string_t[0], string_t[1], "None", "None", "None", "None"])

        df = DataFrame (list_all,columns=lists)
        return df    
    
    # function takes the input as a dataframe and connvert it to Json format based on the sucessful logs with sequence
    def convert_df_to_json(self, df):

        df["counter"] = np.nan
        df["idx"] = np.nan
        counter = 0
        for i in range(df.shape[0]):
            if (df["operation"][i] == "ENTRY"):
                counter += 1
                df["counter"][i] = counter
            elif (df["operation"][i] == "EXIT"):
                counter -= 1
                df["counter"][i] = counter
            else:
                 df["counter"][i] = -1

        index = 1
        for i in range(df.shape[0]):
            if df["counter"][i] >= 1.0:
                df["idx"][i] = index

            if df["counter"][i] == 0.0:
                df["idx"][i] = index
                index +=1

        unique_idx = [x for x in list(dict.fromkeys(df["idx"].tolist())) if str(x) != 'nan']

        dict_full = {} 
        lists = ["operation", "filename", "line_number", "name"]

        df_temp = []
        for i in range(len(unique_idx)):
            df_temp = df.loc[df["idx"] == unique_idx[i]]
            df_temp.drop(['Line no.', 'text','counter', 'idx'], axis = 1, inplace = True) 
            length_df = len(df)+1
            dict_full["result_"+str(i)] = df_temp.to_dict('record')
        return dict_full
    
    # function takes the input as a dataframe and connvert it to Json format based on the sucessful logs with sequence    
    def basic_convert_df_to_json(self, df_filter):    
        dict_f = {}
        df_filter = df_filter[df_filter["operation"] !=  "None"]
        df_filter.drop(['Line no.', 'text'], axis = 1, inplace = True) 
        dict_f["result"] = df_filter.to_dict('record')
        return dict_f
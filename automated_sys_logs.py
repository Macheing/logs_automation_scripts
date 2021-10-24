#!/usr/bin/env python3
# labraries.
import re
import csv
import operator
import sys

def capture_logs(log_file):
    '''
    generates dictionary of system errors and dictionary of users 
    who invoke error events.
    '''
    per_users = {}
    error_counts = {}
    #log_file = open('syslog.log','r')
    # extract info or error messages and users.
    log_patterns = r"(INFO|ERROR)\s([\w*\s*\[#\d+\]']*)\s\(([\w*\.]*)\)"

    with open (log_file,'r') as file:
        for line in file.readlines():
            error_or_info = re.search(log_patterns, line)
            # check if log type is error.
            if error_or_info.group(1) == 'ERROR':
                error = error_or_info.group(1)
                error_message = error_or_info.group(2)
                error_user = error_or_info.group(3)
                error_counts[error_message] =  error_counts.get(error_message,0)+1
                #per_users[error_user]= per_users.get({error_user,error}, 0)+ 1
                # check whether user,error and error_message are already in dictionaries and add 1.
                if error_user in per_users:
                    per_users[error_user][error] +=1
                else:
                    per_users[error_user] = {'INFO':0,'ERROR':1}
 
            # Check if log type is info
            else:
                info = error_or_info.group(1)
                #info_message = error_or_info.group(2)
                info_user = error_or_info.group(3)
                #error_counts[info_message] =  error_counts.get(info_message,0)+1

                if info_user in per_users:
                    per_users[info_user][info] +=1
                else:
                    per_users[info_user] = {'INFO':1,'ERROR':0}
    
    sorted_per_user =sorted(per_users.items(),key=operator.itemgetter(0))
    sorted_error_count = sorted(error_counts.items(),key=operator.itemgetter(1),reverse=True)

    return sorted_per_user,sorted_error_count

def send_to_csv(sorted_per_user,sorted_error_count):
    with open ("user_statistics.csv","w") as users_csv_file:
        writer = csv.writer(users_csv_file)
        writer.writerow(['Username', 'INFO', 'ERROR'])

        for user in sorted_per_user:
            name, type_error = user
            row = [name, type_error['INFO'],type_error['ERROR']]
            writer.writerow(row)

    with open('error_message.csv','w') as error_csv_file:
        writer = csv.writer(error_csv_file)
        writer.writerow(['ERROR','Count'])
        for error in sorted_error_count:
            error_message,count = error
            row = [error_message, count]
            writer.writerow(row)


if __name__ == '__main__':
    log_file = sys.argv[1]
    sorted_per_user,sorted_error_count = capture_logs(log_file)
    send_to_csv(sorted_per_user,sorted_error_count)
    #print(capture_logs(log_file))
    print('Successful!')

    # enter ./automated_sys+logs.py syslog.log




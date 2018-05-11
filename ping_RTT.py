
# This program checks network performance by sending a series of ping requests to the IP mentioned as argument.
# The number of ping requests can be mentioned as argument also.
# This program displays the output in console and creates a json file containing the necessary data
# Author : Soutrik Chatterjee

import argparse
import subprocess
import re
import sys
import platform
import os
import json
import requests
import time

API_ENDPOINT = "http://192.168.14.30/netdash/nettest.php"

# Create a dictionary that will be used to dump json data
dict = {'Location' : ' ' , 'Min' : 0 , 'Max' : 0 , 'Avg' : 0 , 'Loss' : 0}

# JSON output is written to this file
out_file = 'result_json.txt'

def test_round_trip_time(no_of_requests = 20):

    # print('Trying to send {1} ping requests to destination address {0}\n'.format(address, no_of_requests))
    
    # Initialization of minimum, maximum, average round trip times and packet loss
    minimum_rtt = float('Inf')
    maximum_rtt = float('Inf')
    mean_rtt = float('Inf')  
    loss = float('Inf')

    count_flag = '-c'
    if 'win' in sys.platform:
        count_flag = '-n'

    device_ip = ['172.20.8.89', '172.20.64.73', '172.21.48.185',  '172.21.48.181', '172.21.48.201']
    location = ['BTPS', 'KTPS', 'BkTPP', 'SgTPP', 'STPS']
    count = 0

    for address in device_ip :
        print('Pinging address')
        print(address)
        try:
            ping = subprocess.Popen(['ping', address, count_flag, str(no_of_requests)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out,err) = ping.communicate()
            if out and ('win' in sys.platform):
                try:
                    minimum_rtt = int(re.findall(r'Minimum = (\d+)', out)[0])
                    maximum_rtt = int(re.findall(r'Maximum = (\d+)', out)[0])
                    mean_rtt = int(re.findall(r'Average = (\d+)', out)[0])
                    loss = int(re.findall(r'Lost = (\d+)', out)[0])

                    write_to_dict(location[count], minimum_rtt, maximum_rtt, mean_rtt, loss)
                                  
                    write_to_json_file()

                    #count = count + 1

                    #json.dumps(dict)

                    
                except:
                    print('Device unreachable')

                    write_to_dict(location[count], None, None, None, loss)

                    write_to_json_file()

                    #count = count + 1

                    
            elif out:
                try:
                # Linux-specific output parsing
                    summary = re.findall(r'rtt min/avg/max/mdev = (\S+)', out)[0]
                    (minimum_rtt, mean_rtt, maximum_rtt, mdev) = (float(x) for x in summary.split('/'))
                    loss = int(re.findall(r'(\d+)% packet loss', out)[0])

                    write_to_dict(location[count], minimum_rtt, maximum_rtt, mean_rtt, loss)

                    write_to_json_file()

                    #count = count + 1

                    #json.dumps(dict)

                    
                except:
                    print('Device unreachable')

                    write_to_dict(location[count], None, None, None, loss)

                    write_to_json_file()

                    #count = count + 1

            else:
                print('Device unreachable')

                #count = count + 1

        except subprocess.CalledProcessError :
            print('Problem in spawning process')

        count = count + 1
     
	#return(out, minimum_rtt, maximum_rtt, mean_rtt, loss)


def send_data(url, data) :
	# Code to send data to URL Endpoint
	# Send data as a post request
    r = requests.post(url, data)
    print r.text


def write_to_dict(location, min, max, avg, loss) :
    # Write the data to a global dictionary
    dict['Location'] = location
    dict['Min'] = min
    dict['Max'] = max
    dict['Avg'] = avg
    dict['Loss'] = loss

    send_data(API_ENDPOINT, dict)


def write_to_json_file() :
	# Write output as json to a file
    with open(out_file, 'a') as file:
        json.dump(dict, file)




if __name__ == '__main__':
    parser = argparse.ArgumentParser('Checking round-trip time of ping requests')
    # parser.add_argument('-a','--address', help='Target address.', required=True)
    parser.add_argument('-n', help='Number of times to ping.', type=int, default=20)

    args = parser.parse_args()

    # Get time and platform info
    #print('Platform: {0}\n'.format(platform.platform()))
    # Run the ping test
    #(data, min, max, mean, lost) = 

    while True :
        test_round_trip_time(args.n)
        time.sleep(180)

	#print results
    #print('minimum = {0}ms\nmaximum = {1}ms\nmean = {2}ms\nloss = {3}%\n\n'.format(min, max, mean, lost))

    #print(data)



    
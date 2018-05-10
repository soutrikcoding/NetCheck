
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

def test_round_trip_time(address, no_of_requests = 20):
    
    print('Trying to send {1} ping requests to destination address {0}\n'.format(address, no_of_requests))
    
    # Initialization of minimum, maximum, average round trip times and packet loss
    minimum_rtt = float('Inf')
    maximum_rtt = float('Inf')
    mean_rtt = float('Inf')  
    loss = float('Inf')

    count_flag = '-c'
    if 'win' in sys.platform:
        count_flag = '-n'

    try:
        ping = subprocess.Popen(['ping', address, count_flag, str(no_of_requests)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        (out,err) = ping.communicate()
        if out and ('win' in sys.platform):
            try:
                # Windows-specific output parsing
                minimum_rtt = int(re.findall(r'Minimum = (\d+)', out)[0])
                maximum_rtt = int(re.findall(r'Maximum = (\d+)', out)[0])
                mean_rtt = int(re.findall(r'Average = (\d+)', out)[0])
                loss = int(re.findall(r'Lost = (\d+)', out)[0])
            except:
                print('No data for one of minimum_rtt/maximum_rtt/mean_rtt/loss')
        elif out:
            try:
                # Linux-specific output parsing
                summary = re.findall(r'rtt min/avg/max/mdev = (\S+)', out)[0]
                (minimum_rtt, mean_rtt, maximum_rtt, mdev) = (float(x) for x in summary.split('/'))
                loss = int(re.findall(r'(\d+)% packet loss', out)[0])
            except:
                print('No data for one of minimum/maximum/mean/lost')
        else:
            print('No ping')

    except subprocess.CalledProcessError:
        print('Could not get a ping!')

    return(out, minimum_rtt, maximum_rtt, mean_rtt, loss)
	
	
if __name__ == '__main__':
    parser = argparse.ArgumentParser('Checking round-trip time of ping requests')
    parser.add_argument('-a','--address', help='Target address.', required=True)
    parser.add_argument('-n', help='Number of times to ping.', type=int, default=10)
    
    args = parser.parse_args()

    # Get time and platform info
    #print('Platform: {0}\n'.format(platform.platform()))
    
    # Run the ping test
    (data, min, max, mean, lost) = test_round_trip_time(args.address, args.n)
	
	# Create a dictionary that will be used to dump json data
    dict = {'Min' : 0 , 'Max' : 0 , 'Avg' : 0 , 'Loss' : 0}
    dict['Min'] = min
    dict['Max'] = max
    dict['Avg'] = mean
    dict['Loss'] = lost
	
    json.dumps(dict)
	
	# Write output as json
    with open('result_json.txt', 'w') as file:
	    json.dump(dict, file)
   
	#print results
    print('minimum = {0}ms\nmaximum = {1}ms\nmean = {2}ms\nloss = {3}%\n\n'.format(min, max, mean, lost))
	
	

    
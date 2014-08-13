'''
Created on Aug 12, 2014

@author: sscepano
'''
from os.path import join

#######################################################################################      
# this is where we save the extracted data needed for the next steps to .TSV files
####################################################################################### 
def save(data):
    
    print len(data)
    
    location = "/home/sscepano/Project7s/D4D/CI/call_wakeup_sleep_hour"
    file_name = "subpref_morning_10pct.tsv"
    file_name2 = "subpref_morning_15pct.tsv"
    file_name3 = "subpref_morning_XXpct.tsv"
    save_path = join(location,file_name)
    save_path2 = join(location,file_name2)
    save_path3 = join(location,file_name3)
    f = open(save_path, "w")
    f2 = open(save_path2, "w")
    f3 = open(save_path3, "w")
    
    for subpref in data.keys():
        if subpref <> -1 and subpref <> 0:
            f.write(str(subpref) + '\t')
            f2.write(str(subpref) + '\t')
            f3.write(str(subpref) + '\t')
            peak1, peak2 = find_peaks(data[subpref])
            f.write(str(peak1) + '\t' + str(peak2) + '\n')
            if peak1 <> 0:
                f3.write(str(peak2/float(peak1)) + '\n')
            else:
                f3.write(str(float(0)) + '\n')
            peakt1, peakt2 = find_peak_times(data[subpref])
            f2.write(str(peakt1) + '\t' + str(peakt2) + '\n')

    return


def find_peaks(data):
    
    peak1 = 0
    peak2 = 0
    
    for hr in data.keys():
        for minut in data[hr].keys():
            if hr <= 14:
                if data[hr][minut] > peak1:
                    peak1 = data[hr][minut] 
            else:
                if data[hr][minut] > peak2:
                    peak2 = data[hr][minut] 
                    
    return peak1, peak2

def find_peak_times(data):
    
    peak1 = 0
    peak2 = 0
    peakt1 = 0
    peakt2 = 0
    
    for hr in data.keys():
        for minut in data[hr].keys():
            if hr <= 14:
                if data[hr][minut] > peak1:
                    peak1 = data[hr][minut] 
                    peakt1 = (hr, minut)
            else:
                if data[hr][minut] > peak2:
                    peak2 = data[hr][minut] 
                    peakt2 = (hr, minut)
                    
    return peakt1, peakt2

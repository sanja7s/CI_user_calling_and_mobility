'''
Created on Jun 16, 2014

@author: sscepano
'''
from os.path import join

#######################################################################################      
# this is where we save the extracted data needed for the next steps to .TSV files
####################################################################################### 
def save_user_stats(data):
    
    print len(data)
    
    location = "/home/sscepano/Project7s/D4D/CI/user_stats/OUTPUTfiles"
    file_name = "user_frequency_numDistinctSUBPREFvisited.tsv"
#     file_name2 = "users_home.tsv"
    save_path = join(location,file_name)
#     save_path2 = join(location,file_name2)
    f = open(save_path, "w")
#     f2 = open(save_path2, "w")
    
    for user in data.keys():
        f.write(str(user) + '\t')
#         f2.write(str(user) + ':\t')

#######################################################################################
# remove subpref -1 
#######################################################################################
        try:
            data[user]['subpref'].pop(-1)
        except KeyError:
            print user
        f.write(str(data[user]['fq']) + '\t' + str(sum(data[user]['subpref'].values())))
#             f2.write(str(subpref) + '\t') 
        f.write('\n')
#         f2.write('\n')          
    return
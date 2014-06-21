'''
Created on Jun 20, 2014

@author: sscepano
'''
#####################################################################      
# this one is for calculating and saving radius of gyration
#######################################################################################  


def save_traj(data):
    
    avg_usr_traj, usr_traj, usr_day, usr_total_traj = data[0], data[1], data[2], data[3]
    
    file_name = "/home/sscepano/Project7s/D4D/CI/user_stats/Traj/avg_usr_daily_traj.tsv"
    f = open(file_name, "w")
    
    file_name2 = "/home/sscepano/Project7s/D4D/CI/user_stats/Traj/usr_traj.tsv"
    f2 = open(file_name2, "w")
    
    file_name3 = "/home/sscepano/Project7s/D4D/CI/user_stats/Traj/usr_days_active.tsv"
    f3 = open(file_name3, "w")
    
    file_name4 = "/home/sscepano/Project7s/D4D/CI/user_stats/Traj/usr_total_traj.tsv"
    f4 = open(file_name4, "w")
    
    for usr in avg_usr_traj.keys():
        f.write(str(usr) + '\t' + str(avg_usr_traj[usr]) + '\n')
        f2.write(str(usr) + '\t' + str(usr_traj[usr]) + '\n')
        f3.write(str(usr) + '\t' + str(usr_day[usr]) + '\n')
        f4.write(str(usr) + '\t' + str(usr_total_traj[usr]) + '\n')
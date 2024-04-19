import subprocess
from subprocess import Popen, PIPE
import time
import datetime
import warnings
import os
import shutil
import pyzipper

def get_end_time():
    now = datetime.datetime.now()
    print("Enter the hour of the end time (0-23 12 hour format):")
    hour = int(input())
    print("Enter the minute of the end time (0-59):")
    minute = int(input())
    print("Enter the second of the end time (0-59):")
    second = int(input())
    return datetime.datetime(now.year, now.month, now.day, hour, minute, second)

def countdown(stop):
    while True:
        difference = stop - datetime.datetime.now()
        count_hours, rem = divmod(difference.seconds, 3600)
        count_minutes, count_seconds = divmod(rem, 60)
        if difference.days < 0:
            stop += datetime.timedelta(days=1)
        elif difference.days == 0 and count_hours == 0 and count_minutes == 0 and count_seconds == 0:
            print("Countdown finished!")
            print("Initializing Script...")
            time.sleep(1)
            DatabaseBackup()
            print("The Database has now backup. The cycle will continue, thank you!")
            stop += datetime.timedelta(days=1)
        print('Countdown: '
              + str(difference.days) + " day(s) "
              + str(count_hours) + " hour(s) "
              + str(count_minutes) + " minute(s) "
              + str(count_seconds) + " second(s) "
              )
        time.sleep(1)
        stop = stop

def DatabaseBackup():
    # Path to mysqldump executable
    #for server
    mysqldump_path = r'C:\wamp64\bin\mysql\mysql5.7.36\bin\mysqldump.exe'
    #mysqldump_path = r'C:\wamp64\bin\mysql\mysql8.0.31\bin\mysqldump.exe'

    # MySQL server connection details
    host = 'localhost'
    user = 'root'
    password = 'AIOUiojhkn2'

    # Backup directory
    backup_dir = r'\\dir'

    # Get current date and time
    now = datetime.datetime.now()
    date_time = now.strftime('%Y-%m-%d_%H-%M-%S')

    # Backup filename
    backup_file = backup_dir + r'\db.sql'.format(date_time)
    process = Popen([mysqldump_path, '-h', host, '-u', user, '--all-databases', '--result-file=' + backup_file], stdin=PIPE)
    process.communicate(input=password.encode())

    print('Backup completed successfully!')

    # create backup
    desti_file = backup_dir + r'\dir'.format(date_time)
    sql_file = backup_dir + r'\dir.sql'.format(date_time)

    #shutil.make_archive(desti_file, 'zip', backup_dir, sql_file)

    with pyzipper.AESZipFile(desti_file+'.zip', 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(b'password')
        zf.write(sql_file, arcname=os.path.basename(sql_file))

    # Delete the original backup file
    os.remove(backup_file)

    print('Backup file zipped successfully!')

print("The Script is Running")
countdown(get_end_time())
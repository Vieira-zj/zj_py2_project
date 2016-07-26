# -*- coding: utf-8 -*-

'''
Created on 2016-7-20

@author: Vieira

Include the utils on Windows env.

'''

import os
import time
import subprocess
import logging

# --------------------------------------------------------------
# Time functions
# --------------------------------------------------------------
def get_current_date_and_time():
    return time.strftime('%y-%m-%d %H_%M_%S')

def get_current_date():
    return time.strftime('%Y%m%d')


# --------------------------------------------------------------
# Run system commands
# --------------------------------------------------------------
def run_sys_cmd(cmd):
    logging.debug('Run command %s' %cmd)

    ret = os.system(cmd)
    if not ret == 0:
        logging.warn('Failed, run command %s, return code is %d' %(cmd, ret))
        return False

    return True

def run_sys_cmd_and_readlines(cmd):
    logging.debug('Run command %s' %cmd)
    
    lines = os.popen(cmd).readlines()
    if len(lines) == 0:
        logging.warn('The output is null for command %s' %cmd)
        return ''
    
    return lines

def run_sys_cmd_and_read(cmd):
    logging.debug('Run command %s' %cmd)

    content = os.popen(cmd).read()
    if content == None:
        logging.warn('The output is null for command %s' %cmd)
        content = ''

    return content

def run_sys_cmd_in_subprocess(cmd):
    logging.debug('Run command %s' %cmd)

    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    lines_error = p.stderr.readlines()
    lines_output = p.stdout.readlines()

    if len(lines_error) > 0:
        return False,lines_error
    elif len(lines_output) > 0:
        return True,lines_output
    else:
        logging.warn('The output is null for command %s' %cmd)
        return False,''


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
if __name__ == '__main__':

    pass

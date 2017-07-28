# -*- coding: utf-8 -*-
'''
Created on 2016-6-15

@author: zhengjin

Runner to execute multiple monitor scripts concurrently.

'''

import time
import threading

import MonitorUtils as MUtils
import MemMonitorDumpsys, MemMonitorProcrank, CpuMonitorTop

# --------------------------------------------------------------
# Constants
# --------------------------------------------------------------
THREADS_LIST = []  # holds all running threads


# --------------------------------------------------------------
# Env variables setup
# --------------------------------------------------------------
def monitor_runner_env_vars_setup():
    set_env_vars_for_cpu_monitor_top()
    set_env_vars_for_mem_monitor_dumpsys()
    set_env_vars_for_mem_monitor_procrank()

def set_env_vars_for_cpu_monitor_top():
    CpuMonitorTop.g_report_root_path = report_root_path
    CpuMonitorTop.g_pkg_name = pkg_name
    CpuMonitorTop.g_run_num = run_number
    CpuMonitorTop.g_run_time = run_time
    CpuMonitorTop.g_monitor_interval = get_monitor_interval_time()
    CpuMonitorTop.g_is_top_for_pkg = g_is_for_pkg

def set_env_vars_for_mem_monitor_dumpsys():
    MemMonitorDumpsys.g_report_root_path = report_root_path
    MemMonitorDumpsys.g_pkg_name = pkg_name
    MemMonitorDumpsys.g_run_num = run_number
    MemMonitorDumpsys.g_run_time = run_time
    MemMonitorDumpsys.g_monitor_interval = get_monitor_interval_time()

def set_env_vars_for_mem_monitor_procrank():
    MemMonitorProcrank.g_report_root_path = report_root_path
    MemMonitorProcrank.g_pkg_name = pkg_name
    MemMonitorProcrank.g_run_num = run_number
    MemMonitorProcrank.g_run_time = run_time
    MemMonitorProcrank.g_monitor_interval = get_monitor_interval_time()
    MemMonitorProcrank.g_is_process = g_is_for_pkg

def get_monitor_interval_time():
    global monitor_interval
    try:
        return monitor_interval
    except Exception:
        # if 'monitor_interval' does not define
        return MUtils.g_interval


# --------------------------------------------------------------
# Daemon thread main
# --------------------------------------------------------------
def daemon_thread_main():
    g_daemon_thread_sleep_time = 15  # seconds
    while 1:
        print MUtils.g_get_current_time() + ', monitor runner process is running...'
        time.sleep(g_daemon_thread_sleep_time)


# --------------------------------------------------------------
# Build threads
# --------------------------------------------------------------
def build_daemon_thread():
    thread_name = 'monitor:daemon'
    t = threading.Thread(name=thread_name, target=daemon_thread_main)
    t.setDaemon(True)
    return t

def build_thread_mem_monitor_dumpsys():
    thread_name = 'mem:monitor:dumpsys'
    t = threading.Thread(name=thread_name, target=MemMonitorDumpsys.mem_monitor_dumpsys_main)
    return t

def build_thread_mem_monitor_procrank():
    thread_name = 'mem:monitor:procrank'
    t = threading.Thread(name=thread_name, target=MemMonitorProcrank.mem_monitor_procrank_main)
    return t

def build_thread_cpu_monitor_top():
    thread_name = 'cpu:monitor:top'
    t = threading.Thread(name=thread_name, target=CpuMonitorTop.cpu_monitor_top_main)
    return t

def add_thread_to_pool(t):
    THREADS_LIST.append(t)


# --------------------------------------------------------------
# Action threads
# --------------------------------------------------------------
def start_daemon_thread(t_daemon):
    t_daemon.start()

def start_all_threads_in_pool():
    for t in THREADS_LIST:
        t.start()

def wait_all_threads_exit_in_pool():
    for t in THREADS_LIST:
        t.join()


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def monitor_runner_setup():
    t_daemon = build_daemon_thread()
    start_daemon_thread(t_daemon)
    
    add_thread_to_pool(build_thread_cpu_monitor_top())
    if g_is_mem_monitor_by_dumpsys:
        add_thread_to_pool(build_thread_mem_monitor_dumpsys())
    else:
        add_thread_to_pool(build_thread_mem_monitor_procrank())

    monitor_runner_env_vars_setup()
    
def monitor_runner_execution():
    if len(THREADS_LIST) == 0:
        print 'Error, there is no thread in the pool!'
        exit(1)

    start_all_threads_in_pool()
    wait_all_threads_exit_in_pool()

def monitor_runner_clearup():
    del THREADS_LIST[:]

def monitor_runner_main():
    monitor_runner_setup()
    monitor_runner_execution()
    monitor_runner_clearup()


if __name__ == '__main__':

    pkg_name = 'com.bestv.ott'
    run_time = 10 * MUtils.g_min
    monitor_interval = MUtils.g_short_interval
    
    g_is_for_pkg = True
    g_is_mem_monitor_by_dumpsys = False
    
    run_number = '01'
    report_root_path = r'%s\%s_%s' % (MUtils.g_get_report_root_path(), MUtils.g_get_current_date(), run_number)
    
    monitor_runner_main()
    
    print 'Monitor runner DONE!'

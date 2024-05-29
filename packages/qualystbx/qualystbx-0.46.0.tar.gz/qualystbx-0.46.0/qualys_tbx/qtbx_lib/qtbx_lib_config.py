try:
    import psutil
except ImportError:
    pass
import os
import sys
import getpass
import re
from pathlib import Path
from qualys_tbx.qtbx_lib import qtbx_lib_functions
from qualys_tbx.qtbx_lib import qtbx_lib_logger
global qtbx_venv_dir
global qtbx_home_dir
global qtbx_data_dir
global qtbx_log_dir
global qtbx_config_dir
global qtbx_bin_dir
global qtbx_cred_dir
global qtbx_tool_selected_to_run
global qtbx_storage_dir
global qtbx_log_file_path
global qtbx_log_file_rotate_path
global qtbx_log_file_lock_path
global qtbx_log_to_console
global qtbx_rebuild_venv

# def pgrep_af(pattern):
#     matching_processes = []
#     current_pid = os.getpid()
#
#     for process in psutil.process_iter():
#         try:
#             if process.pid == current_pid:
#                 continue
#             cmdline = ' '.join(process.cmdline())
#             if cmdline != '':
#                 if re.search(pattern, cmdline):
#                     matching_processes.append((process.pid, cmdline))
#         except psutil.ZombieProcess:
#             pass
#         except psutil.NoSuchProcess:
#             pass
#         except psutil.AccessDenied:
#             matching_processes.append((process.pid, "Access Denied"))
#
#     return matching_processes

def pgrep_af(pattern):
    matching_processes = []
    current_pid = os.getpid()
    pattern = re.compile(pattern, re.IGNORECASE)  # Making the search case-insensitive
    for process in psutil.process_iter():
        try:
            if process.pid == current_pid:
                continue
            cmdline = ' '.join(process.cmdline())
            if cmdline != '':
                if pattern.search(cmdline):
                    matching_processes.append((process.pid, cmdline))
        except (psutil.ZombieProcess, psutil.NoSuchProcess):
            continue
        except psutil.AccessDenied:
            matching_processes.append((process.pid, "Access Denied"))

    return matching_processes


def log_qtbx_directories():
    qtbx_lib_logger.logger_info(f"qtbx_tool_selected_to_run: {qtbx_tool_selected_to_run}")
    qtbx_lib_logger.logger_info(f"qtbx_storage_dir(virtual env dir): {qtbx_storage_dir}")
    qtbx_lib_logger.logger_info(f"qtbx_home_dir: {qtbx_home_dir}")
    qtbx_lib_logger.logger_info(f"qtbx_bin_dir: {qtbx_bin_dir}")
    qtbx_lib_logger.logger_info(f"qtbx_data_dir: {qtbx_data_dir}")
    qtbx_lib_logger.logger_info(f"qtbx_log_dir: {qtbx_log_dir}")
    qtbx_lib_logger.logger_info(f"qtbx_cred_dir: {qtbx_cred_dir}")

def set_qtbx_directories():
    global qtbx_venv_dir
    global qtbx_home_dir
    global qtbx_data_dir
    global qtbx_log_dir
    global qtbx_config_dir
    global qtbx_bin_dir
    global qtbx_cred_dir
    global qtbx_tool_selected_to_run
    global qtbx_storage_dir

    if qtbx_storage_dir is None:
        print(f"Error: The directory '{qtbx_storage_dir}' is not set. It should be set to your VIRTUAL_ENV variable.  "
              f"\nPlease ensure you have setup your virtual environment according to qualystbx instructions on pypy.org/projects/qualystbx")
        sys.exit(1)

    if qtbx_tool_selected_to_run is None:
        qtbx_tool_selected_to_run = "default"

    if not os.access(qtbx_storage_dir, os.W_OK):
        username = getpass.getuser()
        print(f"Error: The directory '{qtbx_storage_dir}' is not writable. Please ensure directory is writable by user {username}."
              f"\nPlease ensure you have setup your virtual environment according to qualystbx instructions on pypy.org/projects/qualystbx")
        sys.exit(1)

    qtbx_venv_dir = Path(qtbx_storage_dir)
    qtbx_home_dir = Path(qtbx_storage_dir,"qualystbx", "qtbx_home", qtbx_tool_selected_to_run)
    qtbx_data_dir = Path(qtbx_home_dir, "data")
    qtbx_log_dir = Path(qtbx_home_dir, "log")
    qtbx_bin_dir = Path(qtbx_home_dir, "bin")
    qtbx_config_dir = Path(qtbx_home_dir, "config")
    qtbx_cred_dir = Path(qtbx_home_dir, "cred")

def create_qtbx_directories():
    global qtbx_home_dir
    global qtbx_data_dir
    global qtbx_log_dir
    global qtbx_config_dir
    global qtbx_bin_dir
    global qtbx_cred_dir
    global qtbx_tool_selected_to_run
    global qtbx_storage_dir

    qtbx_lib_functions.create_local_directory(qtbx_data_dir)
    qtbx_lib_functions.create_local_directory(qtbx_log_dir)
    qtbx_lib_functions.create_local_directory(qtbx_bin_dir)
    qtbx_lib_functions.create_local_directory(qtbx_config_dir)
    qtbx_lib_functions.create_local_directory(qtbx_cred_dir)

def set_qtbx_log_file_path(file_name=None):
    global qtbx_log_file_path
    global qtbx_log_file_lock_path
    global qtbx_log_file_rotate_path
    if file_name is None:
        qtbx_log_file_path = Path(qtbx_log_dir, "qtbx.log")
    else:
        qtbx_log_file_path = Path(qtbx_log_dir, file_name)

    qtbx_log_file_lock_path = Path(f"{qtbx_log_file_path.__str__()}.lock")
    qtbx_log_file_rotate_path = Path(f"{qtbx_log_file_path.__str__()}.1")

def get_virtualenv_path_and_return_storage_dir():
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        venv_path = os.getenv('VIRTUAL_ENV')
        if venv_path:
            pass
        else:
            print(f"Not in Virtual environment path: {venv_path}")
            print(f"Please enter your virtual environment, or recreate it using the instructions at pypy.org/projects/qualystbx")
            exit(1)

    else:
        username = getpass.getuser()
        if username == 'dgregory': # For testing in Pycharm until bug fix for virtual env in pycharm.
            venv_path = os.path.expanduser('~')
        else:
            print("Not in a Python virtual environment")
            print(
                f"Please enter your virtual environment, or recreate it using the instructions at pypy.org/projects/qualystbx")
            exit(1)

    print(f"Storage Directory (Python Virtual Environment): {venv_path}")
    return venv_path

# Example usage
if __name__ == "__main__":
    qtbx_lib_logger.set_logger()
    create_qtbx_directories()
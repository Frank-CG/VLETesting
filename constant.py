from os.path import realpath, dirname, split

PROJECT_ROOT_DIR = dirname(dirname(realpath(__file__))) # This is Project Root
LOG_DIR = str(PROJECT_ROOT_DIR) + "/logs/"
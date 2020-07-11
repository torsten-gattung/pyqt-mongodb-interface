import functions as fn

from FrontendLoader import start_program


global_vars:dict = fn.load_json_file_as_dict("GLOBAL_VARIABLES.json")
widget_ids:dict = fn.load_json_file_as_dict("WIDGET_ID.json")

start_program(widget_ids, global_vars['GUI_FILE_PATH'])

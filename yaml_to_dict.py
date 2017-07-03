import yaml

def yaml_dict_py (yaml_file, py_file, dict_name):
    str_yaml = open(yaml_file).read()
    dict_yaml = yaml.load (str_yaml.replace('\t','  '))
    f_out = open (py_file,'w')
    f_out.write (dict_name + ' = ' + repr(dict_yaml) + '\n')
    f_out.close()


yaml_dict_py ('nouns_test.yml','nouns_test.py','dict_txt_nouns')
yaml_dict_py ('dialogs.yml','dialogs.py','dict_txt_dialogs')
yaml_dict_py ('interaction.yml','interaction.py','dict_txt_interaction')

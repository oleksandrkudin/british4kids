"""
There is error in yaml module for Android platform.
This module convert yaml files to dictionary what are saved in .py files.
"""

import yaml

def yaml_dict_py(yaml_file, py_file, dict_name):
    """read configuration from yaml file to dict and save if in .py file"""
    str_yaml = open(yaml_file).read()
    dict_yaml = yaml.load(str_yaml.replace('\t', '  '))
    f_out = open(py_file, 'w')
    f_out.write(dict_name + ' = ' + repr(dict_yaml) + '\n')
    f_out.close()


# Previous version of application
# IT STILL WORKS
#yaml_dict_py('nouns_test.yml', 'nouns_test.py', 'dict_txt_nouns')
yaml_dict_py('dialogs.yml', 'dialogs.py', 'dict_txt_dialogs')
yaml_dict_py('interaction.yml', 'interaction.py', 'dict_txt_interaction')

# New version with new class architechture
yaml_dict_py('nouns.yml', 'nouns.py', 'dict_txt_nouns')
yaml_dict_py('auxiliary_words.yml', 'auxiliary_words.py', 'dict_txt_auxiliary_words')

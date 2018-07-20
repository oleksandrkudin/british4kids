"""
Remove ending white spaces for each line in the file
"""

def file_strip(file_name):
    new_lines = [line.rstrip() for line in open(file_name)]
    #list(map(print, ))
    new_file = open('~' + file_name, 'w')
    for line in new_lines:
        new_file.write(line+'\n')
    new_file.close()
        
    #for line in open(file_name):
    #    print(line.rstrip())

if __name__ == '__main__':
    file_strip('grammarsentence.py')

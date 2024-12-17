
def write_file(file):
    with open("file1.txt", 'w', encoding='utf-8') as f:
        f.write('\n'.join(file.split('.')))

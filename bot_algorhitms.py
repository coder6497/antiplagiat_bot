import os

def check_file():
    with open(f"files/{os.listdir("files")[0]}", 'r', encoding='utf-8') as f:
        data = f.read().split('\n')
    with open(f"files/{os.listdir("files")[1]}", 'r', encoding='utf-8') as f:
        data2 = f.read().split('\n')
    count = 0
    for i in range(len(data)):
        for j in range(len(data2)):
            if data[i] == data2[j]:
                count += 1
    return count

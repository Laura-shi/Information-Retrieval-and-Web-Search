source_file=open("source.txt",mode='r',encoding='utf-8')
destination_file=open("destination.txt",mode='w',encoding='utf-8')

content = source_file.readlines()

for line in content:
    destination_file.write(line)

source_file.close()
destination_file.close()
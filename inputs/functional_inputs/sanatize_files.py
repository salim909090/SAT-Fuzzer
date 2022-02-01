import os
inputs_path = "."
if not os.path.exists(inputs_path):
    print("[!] Input path given does not exist")
    exit
input_files = [f for f in os.listdir(inputs_path) if os.path.join(inputs_path, f)]
# input_file = random.choice(input_files)
# print(input_file)
for i_file in input_files:
    if i_file == "sanatize_files.py":
        exit()
    file = open(i_file,"r")
    output = ""
    for line in file.readlines():
        if line.startswith("c"):
            continue
        else:
            output += line
    file.close()
    file = open(i_file,'w')
    file.write(output)
    file.close()


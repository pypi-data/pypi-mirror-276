def check_file(file, file_content_file):
    with open(file, "r") as file1:
        read_file = file1.read()
        act_file = open(file_content_file, "r")
        read_act_file = act_file.read()
        if read_file != read_act_file:
            update_file(file, file_content_file)

def update_file(file, file_content_file):
    with open(file,"w") as real_file:
        act_file = open(file_content_file, "r")
        read_act_file = act_file.read()
        try:
            real_file.write(read_act_file)
        except Exception as e:
            print(f"Error: {e}")
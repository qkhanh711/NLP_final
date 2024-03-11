import os

def test():
    path = "NLP_final/vnexpress_data_summarization/original/Cluster_001/original/1.txt"

    with open(path, "r") as f:
        src = f.readlines()
        src = src[6]
        title = src[:8]
        src = src[8:]
        print(src)
        if src == "None" or src == "N/A" or src == "":
            print(" File does not have summary")
        else:
            print(f"{title}",src)

def check_summary(path):
    with open(path, "r") as f:
        src = f.readlines()
        src = src[6]
        title = src[:8]
        src = src[8:]
        # print(src[:5])
        if len(src) < 20:
            return False
        else:
            return True
        
def check_content(path):
    with open(path, "r") as f:
        src = f.readlines()
        src = src[7]
        title = src[:9]
        src = src[9:]
        # print(src[:5])
        if len(src) < 20:
            return False
        else:
            return True

num_cluster = os.listdir("NLP_final/vnexpress_data_summarization/original")
print(len(num_cluster))

num_files_in_clus = [len(os.listdir(f"NLP_final/vnexpress_data_summarization/original/Cluster_{i+1:03}/original")) for i in range(len(num_cluster))]
print(num_files_in_clus)
print("Number files before cleaning: ", sum(num_files_in_clus))

for i in range(len(num_cluster)):
    num_files = num_files_in_clus[i]
    for j in range(num_files):
        path = f"NLP_final/vnexpress_data_summarization/original/Cluster_{i+1:03}/original/{j+1}.txt"
        # print(f"File {j+1:03} in Cluster {i+1:03} has summary: {check_summary(path)} and content: {check_content(path)}")
        if check_summary(path) == False or check_content(path) == False:
            remove_path = f"NLP_final/vnexpress_data_summarization/original/Cluster_{i+1:03}/original/{j+1}.txt"
            os.remove(remove_path)
            print(f"File {j+1:03} in Cluster {i+1:03} has been removed")
        # else:
            # print(f"File {j+1:03} in Cluster {i+1:03} is valid")

print("Number files after cleaning: ", sum([len(os.listdir(f"NLP_final/vnexpress_data_summarization/original/Cluster_{i+1:03}/original")) for i in range(len(num_cluster))]))
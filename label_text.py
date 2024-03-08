import os 
from utils.utils import Labeler
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Label news and summary')
parser.add_argument('--threshold', type=int, default=20, help='Threshold to label')

args = parser.parse_args()
threshold = args.threshold

def test():
    path_origin  = "./vnexpress_data_summarization/original/Cluster_001/original/1.txt"
    path_summary = "./vnexpress_data_summarization/summary/Cluster_001/summary/0.gold.txt"   
    labeler = Labeler(path_origin, path_summary)
    results = labeler.get_all()
    print(results['news'])
    print(results['summary'])
    print(results['labels'])

num_cluster = os.listdir("vnexpress_data_summarization/original")
print(len(num_cluster))



for i in tqdm(range(1, len(num_cluster)+1)):
    path_origin  = f"vnexpress_data_summarization/original/Cluster_{i:03}/original/1.txt"
    path_summary_0 = f"vnexpress_data_summarization/summary/Cluster_{i:03}/0.gold.txt"   
    path_summary_1 = f"vnexpress_data_summarization/summary/Cluster_{i:03}/1.gold.txt"
    labeler0 = Labeler(path_origin, path_summary_0, threshold=threshold)
    results0 = labeler0.get_all()
    labeler1 = Labeler(path_origin, path_summary_1, threshold=threshold)
    results1 = labeler1.get_all()
    if not os.path.exists(f"vnexpress_data_summarization/S3_summary/Cluster_{i:03}"):
        os.makedirs(f"vnexpress_data_summarization/S3_summary/Cluster_{i:03}")
    with open(f"vnexpress_data_summarization/S3_summary/Cluster_{i:03}/0.s3.txt", "w", encoding="utf-8") as f:
        for index in range(len(results0['news'])):
            if results0["news"][index].strip() == "":
                f.write("\n")
            else:
                f.write(str(results0["labels"][index]) + "   " + results0["news"][index] + "\n")
        f.write("\n")

    with open(f"vnexpress_data_summarization/S3_summary/Cluster_{i:03}/1.s3.txt", "w", encoding="utf-8") as f:
        for index in range(len(results1['news'])):
            if results1["news"][index] == "\n":
                f.write("\n")
            else:
                f.write(str(results1["labels"][index]) + "   " + results1["news"][index] + "\n")
        f.write("\n")

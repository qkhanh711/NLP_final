from rouge_score import rouge_scorer
import os 

scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL', 'rougeLsum'], use_stemmer=True)

def compute(reference, prediction):
    scores = scorer.score(target=reference, prediction=prediction)
    return scores['rouge1'], scores['rouge2'], scores['rougeL'], scores['rougeLsum']

def test():
    path_summary_human = "../vnexpress_data_summarization/summary/Cluster_001/0.gold.txt"
    path_summary_model = "../vnexpress_data_summarization/summary/Cluster_001/1.gold.txt"

    prediction = open(path_summary_model, "r").read()
    reference = open(path_summary_human, "r").read()

    rouge1, rouge2, rougeL, rougeLsum = compute(reference, prediction)

def writer(rouge1, rouge2, rougeL, rougeLsum, save_path):
    with open(save_path, "w") as f:
        f.write(f"Rouge1   : {rouge1}\n")
        f.write(f"Rouge2   : {rouge2}\n")
        f.write(f"RougeL   : {rougeL}\n")
        f.write(f"RougeLsum: {rougeLsum}\n")

num_cluster = os.listdir("vnexpress_data_summarization/summary")

for i in range(len(num_cluster)):
    path_summary_human = f"vnexpress_data_summarization/summary/Cluster_{i+1:03}/0.gold.txt"
    path_summary_model = f"vnexpress_data_summarization/summary/Cluster_{i+1:03}/1.gold.txt"
    prediction = open(path_summary_model, "r").read()
    reference = open(path_summary_human, "r").read()
    rouge1, rouge2, rougeL, rougeLsum = compute(reference, prediction)
    save_path = f"vnexpress_data_summarization/rouge/Cluster_{i+1:03}/rouge.txt"
    if not os.path.exists(f"vnexpress_data_summarization/rouge/Cluster_{i+1:03}"):
        os.makedirs(f"vnexpress_data_summarization/rouge/Cluster_{i+1:03}")
    writer(rouge1, rouge2, rougeL, rougeLsum, save_path)
    print(f"File rouge in Cluster {i+1:03} has been computed")
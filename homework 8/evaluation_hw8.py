def calculate_precision_at_k(relevant_documents, retrieved_documents, k):
    relevant_in_top_k = set(relevant_documents) & set(retrieved_documents[:k])
    return len(relevant_in_top_k) / k if k > 0 else 0

def calculate_recall_at_k(relevant_documents, retrieved_documents, k):
    relevant_in_top_k = set(relevant_documents) & set(retrieved_documents[:k])
    return len(relevant_in_top_k) / len(relevant_documents) if len(relevant_documents) > 0 else 0

def calculate_f1_score(precision, recall):
    return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

def calculate_average_metrics(queries, relevance_judgments):
    total_precision = 0
    total_recall = 0
    total_f1_score = 0

    for query_name in queries:
        relevant_documents = relevance_judgments[query_name]
        retrieved_documents = queries[query_name]  # Replace this with your actual retrieval results

        # Calculate precision, recall, and F1 score at a specified retrieval depth 

        # Evaluate at different values of k
        for k in [1, 5, 10, 20]:
            precision_at_k = calculate_precision_at_k(relevant_documents, retrieved_documents, k)
            recall_at_k = calculate_recall_at_k(relevant_documents, retrieved_documents, k)
            f1_score_at_k = calculate_f1_score(precision_at_k, recall_at_k)

            print('------------------------------------')
            print(f'Evaluation for {query_name} at k={k}:')
            print(f'Precision@{k}: {precision_at_k:.2f}')
            print(f'Recall@{k}: {recall_at_k:.2f}')
            print(f'F1@{k}: {f1_score_at_k:.2f}')

        total_precision += precision_at_k
        total_recall += recall_at_k
        total_f1_score += f1_score_at_k

    # Calculate average precision, recall, and F1 score across all queries
    avg_precision = total_precision / len(queries)
    avg_recall = total_recall / len(queries)
    avg_f1_score = total_f1_score / len(queries)

    return avg_precision, avg_recall, avg_f1_score


def main():

    queries = {
        'q1': [1116,6309,9323,1646,4914,306,711,3430,7937,8623,2278,1036,631,3350,226,4834,6229,7859,9243,1566],   # Retrieval results for data science director
        'q2': [1343,1225,9840,3860,5911,9645,4322,8442,8717,813,2736,1269,2048,8587,7161,1280,6411,9425,7634,3581],   # Retrieval results for president of university of memphis
        'q3': [9494,9874,9858,5775,5656], # retrieval results for plagiarism
        'q4': [8570,8554,852,3006,9909,8916,4981,1308,373,7448,8583,8853,5347,2793,1246,9390,8359,1778,9556,9059], # Retrieval results for learner data institute
        'q5': [7089,3934,3926,3868,3925,3940,3927,3935,3864,3928,3941,3949,4540,2202,2234,6616,7078,7091,4520,2520], #Retrieval results for international student life
        'q6': [9218,4809,1541,6204,7832,606,1011,201,3325,4812,6207,3326,204,1542,4811,1014,1543,606,1013,9221], # Retrieval resuls for music school admission
        'q7': [],
        'q8': [ 2374,1781,7544,7638,4332,1813,8598,3871,3031,8050,9536,412,1801,7,6804,7399,1790,8252,1347,1805], #Retrieval results for college of arts and sciences dean
        'q9': [88801,8872,8808,8722,9470,6044,8425,8764,5055,9690,3560,2856,8488,8409,8393,3005,4301,5650,5769,1381], # Retrieval results for college of fedex institute of technology
        'q10': [5943,7045,7228,7050,7233,6747,2213,1375,7159,7230,2577,7047,8758,7220,6451,3554,3706,1771,6999,7360] # Retrieval results for to be or not to be

    }

    relevance_judgments = {
        'q1': [],  # Ground truth for data science director
        'q2': [],  # Ground truth for president of university of memphis
        'q3': [5775,5656], # Ground truth fro plagiarism
        'q4': [], # Ground truth for learner data institute
        'q5' : [7089], # Ground truth for international student life
        'q6': [9218,4809,1541,6204,7832,606,1011,201,3325], # Ground truth for music school admission 
        'q7': [],
        'q8': [], #Ground truth for college of arts and science dean
        'q9': [8872,8808,8722,9470,6044,8425,8764,5055,9690,3560,2856,8488,8409,8393,3005,4301,5650,5769,1381], #Ground truth for fedex institute of technology
        'q10': [5943,7228,7050,7233,6747,2213] #Ground truth for to be or not to be
    }

    avg_precision, avg_recall, avg_f1_score = calculate_average_metrics(queries, relevance_judgments)

    print('--------------------------')
    print(f'Average Precision: {avg_precision:.2f}')
    print(f'Average Recall: {avg_recall:.2f}')
    print(f'Average F1 Score: {avg_f1_score:.2f}')


if __name__ == "__main__":
    main()
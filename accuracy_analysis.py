import json
import os
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio()

def calculate_accuracy(extracted_data, ground_truth):
    field_accuracies = {}
    total_fields = 0
    similarity_threshold = 0.85

    for key in ['company_name', 'date', 'address', 'total_amount']:
        if key in ground_truth and key in extracted_data:
            similarity = similar(str(ground_truth[key]), str(extracted_data[key]))
            field_accuracies[key] = {
                'similarity': similarity,
                'match': similarity >= similarity_threshold,
                'ground_truth': ground_truth[key],
                'extracted': extracted_data[key]
            }
            total_fields += 1

    overall_accuracy = sum(1 for f in field_accuracies.values() if f['match']) / total_fields if total_fields > 0 else 0
    return field_accuracies, overall_accuracy

def main():
    output_dir = "output"
    
    try:
        with open("ground_truths.json", "r") as f:
            ground_truths = json.load(f)
    except Exception as e:
        print(f"Error loading ground truths: {str(e)}")
        return

    results_summary = {
        'total_files': 0,
        'processed_files': 0,
        'overall_accuracy': 0,
        'field_level_stats': {
            'company_name': {'correct': 0, 'total': 0},
            'date': {'correct': 0, 'total': 0},
            'address': {'correct': 0, 'total': 0},
            'total_amount': {'correct': 0, 'total': 0}
        },
        'detailed_results': []
    }

    for filename in os.listdir(output_dir):
        if filename.endswith('.json') and filename != "processing_summary.json":
            results_summary['total_files'] += 1
            
            with open(os.path.join(output_dir, filename), 'r') as f:
                extracted_data = json.load(f)
            
            if extracted_data['filename'] in ground_truths:
                results_summary['processed_files'] += 1
                ground_truth = ground_truths[extracted_data['filename']]
                
                field_accuracies, overall_accuracy = calculate_accuracy(extracted_data, ground_truth)
                
                file_result = {
                    'filename': extracted_data['filename'],
                    'overall_accuracy': overall_accuracy,
                    'field_accuracies': field_accuracies
                }
                
                results_summary['detailed_results'].append(file_result)
                

                for field, accuracy in field_accuracies.items():
                    results_summary['field_level_stats'][field]['total'] += 1
                    if accuracy['match']:
                        results_summary['field_level_stats'][field]['correct'] += 1


    if results_summary['processed_files'] > 0:
        results_summary['overall_accuracy'] = sum(
            result['overall_accuracy'] for result in results_summary['detailed_results']
        ) / results_summary['processed_files']


    with open(os.path.join(output_dir, 'accuracy_analysis.json'), 'w') as f:
        json.dump(results_summary, f, indent=2)


    print("\nAccuracy Analysis Summary:")
    print(f"Total files processed: {results_summary['processed_files']}/{results_summary['total_files']}")
    print(f"Overall accuracy: {results_summary['overall_accuracy']:.2%}")
    print("\nField-level accuracy:")
    for field, stats in results_summary['field_level_stats'].items():
        if stats['total'] > 0:
            accuracy = stats['correct'] / stats['total']
            print(f"{field}: {accuracy:.2%} ({stats['correct']}/{stats['total']})")

if __name__ == "__main__":
    main()
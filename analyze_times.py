import json
import os

def analyze_processing_times():
    try:
        output_dir = "output"
        results = []
        
        for filename in os.listdir(output_dir):
            if filename.endswith('.json') and filename != "processing_summary.json":
                with open(os.path.join(output_dir, filename), 'r') as f:
                    result = json.load(f)
                    if 'processing_time' in result:
                        results.append(result)
        
        if not results:
            print("No results found to analyze")
            return
            
        total_time = sum(result['processing_time'] for result in results)
        avg_time = total_time / len(results)
        max_time = max(result['processing_time'] for result in results)
        min_time = min(result['processing_time'] for result in results)
        
        print("\nProcessing Time Analysis:")
        print(f"Average Processing Time: {avg_time:.2f} seconds")
        print(f"Maximum Processing Time: {max_time:.2f} seconds")
        print(f"Minimum Processing Time: {min_time:.2f} seconds")
        print(f"Total Processing Time: {total_time:.2f} seconds")
        print(f"Number of files processed: {len(results)}")
        
    except Exception as e:
        print(f"Error analyzing processing times: {str(e)}")

if __name__ == "__main__":
    analyze_processing_times()
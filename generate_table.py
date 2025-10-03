import json
import os
from tabulate import tabulate

def generate_processing_time_table():
    """Generate and display processing time table."""
    output_dir = "output"
    table_data = []
    
    try:
        for filename in os.listdir(output_dir):
            if filename.endswith('.json') and filename != "processing_summary.json":
                with open(os.path.join(output_dir, filename), 'r') as f:
                    result = json.load(f)
                    if 'processing_time' in result:
                        table_data.append([
                            result['filename'],
                            f"{result['processing_time']:.2f}s"
                        ])
        
        table_data.sort(key=lambda x: x[0])
        
        if table_data:
            avg_time = sum(
                float(row[1].replace('s', '')) 
                for row in table_data
            ) / len(table_data)
            
            table_data.append([
                "AVERAGE",
                f"{avg_time:.2f}s"
            ])
        
        print("\nProcessing Time Analysis:")
        print(tabulate(
            table_data,
            headers=["Filename", "Processing Time"],
            tablefmt="grid"
        ))
        
        with open(os.path.join(output_dir, "processing_times_table.txt"), "w") as f:
            f.write(tabulate(
                table_data,
                headers=["Filename", "Processing Time"],
                tablefmt="grid"
            ))
            
    except Exception as e:
        print(f"Error generating processing time table: {str(e)}")

if __name__ == "__main__":
    generate_processing_time_table()
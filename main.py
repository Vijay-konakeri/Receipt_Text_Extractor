import os
import json
import time
import torch
from PIL import Image
from io import BytesIO
import boto3
from process_receipts import process_receipt
from analyze_times import analyze_processing_times
from accuracy_analysis import main as accuracy_analysis_main
from generate_table import generate_processing_time_table

s3 = boto3.client('s3')


bucket_name = 'your-bucket-name'
folder_path = 'your-folder-path'


try:
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        "Qwen/Qwen2-VL-2B-Instruct",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    ).to("cuda" if torch.cuda.is_available() else "cpu")
    processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-2B-Instruct")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Model loaded successfully. Using device: {device}")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    raise

# Create output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)


try:
    print(f"Listing objects in bucket: {bucket_name} with prefix: {folder_path}")
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)
    
    if 'Contents' not in response:
        print(f"No objects found in bucket {bucket_name} with prefix {folder_path}")
        print("Response:", response)
    
    image_keys = [
        obj['Key'] for obj in response.get('Contents', [])
        if obj['Key'].lower().endswith(('.jpg', '.jpeg', '.png'))
    ]
    print(f"Found {len(image_keys)} images to process")
except Exception as e:
    print(f"Error listing S3 objects: {str(e)}")
    raise

summary = []
successful_count = 0

for image_key in image_keys:
    print(f"\nProcessing {image_key}...")
    try:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
        
        image_obj = s3.get_object(Bucket=bucket_name, Key=image_key)
        image_data = image_obj['Body'].read()
        image = Image.open(BytesIO(image_data)).convert('RGB')
        
        result = process_receipt(image, image_key, model, processor, device)
        if result:
            json_filename = os.path.splitext(os.path.basename(image_key))[0] + '.json'
            json_path = os.path.join(output_dir, json_filename)
            

            with open(json_path, 'w') as f:
                json.dump(result, f, indent=2)
            
            summary.append({
                'image_key': image_key,
                'json_file': json_filename,
                'status': 'success'
            })
            successful_count += 1
            print(f"Saved result to {json_path}")
            
    except Exception as e:
        print(f"Error processing {image_key}: {str(e)}")
        summary.append({
            'image_key': image_key,
            'status': 'failed',
            'error': str(e)
        })
        continue


try:
    summary_path = os.path.join(output_dir, "processing_summary.json")
    with open(summary_path, "w") as f:
        json.dump({
            'total_images': len(image_keys),
            'successful': successful_count,
            'failed': len(image_keys) - successful_count,
            'details': summary
        }, f, indent=2)
    print(f"\nSummary saved to {summary_path}")
    print(f"Successfully processed {successful_count} out of {len(image_keys)} images")
except Exception as e:
    print(f"Error saving summary: {str(e)}")


analyze_processing_times()
accuracy_analysis_main()
generate_processing_time_table()
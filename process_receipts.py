import time
import json
import torch

def process_receipt(image, image_name, model, processor, device):
    """Process a single receipt image using Qwen2-VL model"""
    try:
        start_time = time.time()
        messages = [{
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": "Extract the following information from this receipt: company name, date, address, total amount. Format the output as JSON."}
            ]
        }]

        text_prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
        inputs = processor(
            text=[text_prompt],
            images=[image],
            padding=True,
            return_tensors="pt"
        )
        inputs = inputs.to(device)
        
        output_ids = model.generate(**inputs, max_new_tokens=1024)
        generated_ids = [
            output_ids[len(input_ids):] 
            for input_ids, output_ids in zip(inputs.input_ids, output_ids)
        ]
        output_text = processor.batch_decode(
            generated_ids, 
            skip_special_tokens=True, 
            clean_up_tokenization_spaces=True
        )[0]
        
        raw_json_str = output_text.strip('`json\n')
        receipt_data = json.loads(raw_json_str)
        
        receipt_data['filename'] = image_name
        receipt_data['processing_time'] = time.time() - start_time
        
        return receipt_data

    except Exception as e:
        print(f"Error processing {image_name}: {str(e)}")
        return None
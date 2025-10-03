
# Receipt Processing and Analysis

This project processes receipt images to extract information such as company name, date, address, and total amount using a pre-trained model. It also analyzes the processing times and calculates the accuracy of the extracted data against ground truth values.

## Project Structure

- `main.py`: The main script to run the entire process.
- `process_receipts.py`: Contains the function to process individual receipts.
- `analyze_times.py`: Contains the function to analyze processing times.
- `accuracy_analysis.py`: Contains the function to calculate accuracy.
- `generate_table.py`: Contains the function to generate the processing time table.
- `ground_truths.json`: Contains the ground truth data for accuracy analysis.
- `requirements.txt`: List of dependencies.

## Input Data

The input data images are fetched from a GitHub repository. You can access the images from the following link:
[Input Data Images](https://github.com/zzzDavid/ICDAR-2019-SROIE/tree/master/data/img)


## Setup and Installation

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up AWS credentials:**  
   Ensure your AWS credentials are configured properly to access the S3 bucket.

## Usage

1. **Run the main script:**
   ```sh
   python main.py
   ```

2. **Analyze processing times:**  
   The processing times will be analyzed and printed to the console.

3. **Calculate accuracy:**  
   The accuracy of the extracted data will be calculated and saved to `output/accuracy_analysis.json`.

4. **Generate processing time table:**  
   A table of processing times will be generated and saved to `output/processing_times_table.txt`.

## Output

- Individual JSON files for each processed receipt will be saved in the `output` directory.
- A summary of the processing will be saved to `output/processing_summary.json`.
- Accuracy analysis results will be saved to `output/accuracy_analysis.json`.
- Processing time table will be saved to `output/processing_times_table.txt`.

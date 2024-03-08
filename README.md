# Author Nguyen Quoc Khanh

# Install Dependencies:

    pip install -r requirements.txt

## To crawl data from VNexpress to local, run:

    python crawl_Summarization.py --nums_clusters "default = 10"

To clean data:

    python cleaner.py

To creat dataset, run:

    python summary_text.py
    python label_text.py

## Then test compute Rouge score:

    python ComputeRouge.py

Or u can run the run.sh

    bash ./run.sh

## Run command line:

    streamlit run inference/summary_input_tag.py

To see the deployment
```bash
project_name/
│
├── config/
│   ├── __init__.py
│   └── rulesets.json
│   └── settings.py            # Configuration settings, e.g., Azure connection strings, container 
│
├── data/
│   ├── input/                 # Local directory for test input files, if any (ignored by git)
│   └── output/
│       └── hits.csv           # Output CSV file (consider ignoring large data files in git)
│       └── manifest.csv       # Output CSV file (consider ignoring large data files in git)
│
├── src/
│   ├── __init__.py
│   ├── main.py                # Main script to orchestrate the processing
│   ├── azure_blob_utils.py    # Utilities for Azure Blob Storage operations
│   └── text_processing.py     # Text processing logic, including flashtext usage
│
│
├── tests/                      # Unittests
│   ├── __init__.py
│
├── .gitignore                 # Standard gitignore file (include data/input/, data/output/, and .env)
├── requirements.txt           # Project dependencies
├── .env                       # Define environment variables
└── README.md                  # Project overview, setup instructions, and usage guide
```
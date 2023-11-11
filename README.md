# pcmpuncher
Step 1: 
  - Create a .env to root directory
  - Content has :
      - GC_DRIVER_PATH = path
      - USER_NAME = 'user'
      - USER_PASS = 'pass'
      - USER_PIN = 'pin'

Step 2:
  - Save pcm-device-token from browser
  - Create a CSV called 'pcm_cookies.csv' with 4 columns
      - name,value,domain,path
  - Load the values in the next row

Step 3: 
  - pip install all the modules
    - Directly into folder OR create a .venv

Optional:
  - CREATE a .bat FILE
  - The <path_to_directory>\pcmpuncher is the folder where .venv is located
   ```
    @echo off
    cd "<path_to_directory>\pcmpuncher"
    REM Activate the virtual environment
    call .venv\Scripts\activate
    
    REM Run your Python script
    python clock_out\chrome.py
   ```
------------------------------------------------------------------------------
OR:
  - Run on VSCODE (more resource intensive)
  - Run on CMD from root directory (where .venv is located)
    ```
    .venv/scripts/activate
    python clock_out/chrome.py
    ```

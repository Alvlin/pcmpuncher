# pcmpuncher
Step 1: 
  - Modify .env file in root directory
    - Put Paycom information here
      - USER_NAME = 'paycomUser'
      - USER_PASS = 'paycomPass'
      - USER_PIN = 'pin'

Step 2:
  - Save pcm-device-token from browser
    - ![image](https://github.com/user-attachments/assets/6bb9df5a-8a0b-437f-848b-eee6c9e80737)  
  - Modify file 'data/pcm_cookies.csv' with your cookie values
      - name,value,domain,path
      - pcm-device-token-xxxx, yyyy, www.paycomonline.net, /


Step 3a: 
  - Open Terminal & Navigate to pcmpuncher folder
  - run:
      ```
      python -m venv ./.venv
      ```
      
Step 3b:
  - In the Terminal at "./pcmpuncher/"  : run 
    ```
    .venv\scripts\activate
    ```
  - run 
    ```
    pip install -r pip_installs.txt
    ```

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

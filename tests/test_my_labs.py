import os, subprocess, time

base_directory = os.path.join(os.getcwd(), "self-guided-labs")

def test_lab_02():
    notebook_path = base_directory + '/level-1/lab-02-advanced-prompt-engineering/prompt_engineering_challenge.ipynb'
    result = subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', notebook_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{notebook_path} - The lab notebook did not run with error \n {result.stderr}"

def test_lab_05():
    notebook_path = base_directory + '/level-1/lab-05-watsonxai-and-langchain/watsonxai-and-langchain.ipynb'
    result = subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', notebook_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{notebook_path} - The lab notebook did not run with error \n {result.stderr}"

def test_lab_06():
    notebook_1_path = base_directory + '/level-1/lab-06-retrieval-agumented-generation/rag-chromadb-flan.ipynb'
    result = subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', notebook_1_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{notebook_1_path} - The lab notebook did not run with error \n {result.stderr}"

    notebook_2_path = base_directory + '/level-1/lab-06-retrieval-agumented-generation/rag-pdf.ipynb'
    result = subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', notebook_2_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{notebook_2_path} - The lab notebook did not run with error \n {result.stderr}"

def test_lab_07():
    # test if the app runs
    script_path = base_directory + '/level-1/lab-07-watsonxai-demo-with-streamlit/app.py'
    process = subprocess.Popen(["streamlit", "run", script_path, "--server.headless=true"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    time.sleep(5)
    process.terminate() 
    stdout, stderr = process.communicate()
    assert process.returncode == 0, f"{script_path} - The app did not run with error \n {stderr.decode()}"

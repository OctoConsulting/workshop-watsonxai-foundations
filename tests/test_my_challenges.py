import os, subprocess, time

base_directory = os.path.join(os.getcwd(), "self-guided-labs")

def test_challenge_01():
    notebook_path = base_directory + '/apply-lessons-learned/challenge-01/news-article-classification.ipynb'
    result = subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', notebook_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{notebook_path} - The challenge notebook did not run with error \n {result.stderr}"


def test_challenge_04():
    script_path = base_directory + '/apply-lessons-learned/challenge-04/app.py'
    process = subprocess.Popen(["streamlit", "run", script_path, "--server.headless=true"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    time.sleep(5)
    process.terminate() 
    stdout, stderr = process.communicate()
    assert process.returncode == 0, f"{script_path} - The app did not run with error \n {stderr.decode()}"

def test_challenge_04_advanced():
    script_path = base_directory + '/apply-lessons-learned/challenge-04-advanced/app.py'
    process = subprocess.Popen(["streamlit", "run", script_path, "--server.headless=true"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    time.sleep(5)
    process.terminate() 
    stdout, stderr = process.communicate()
    assert process.returncode == 0, f"{script_path} - The app did not run with error \n {stderr.decode()}"

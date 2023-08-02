import os, subprocess

base_directory = os.path.join(os.getcwd(), "self-guided-labs")

def test_lab_02():
    lab_name= "lab 02"
    notebook_path = base_directory + '/level-1/lab-02-advanced-prompt-engineering/prompt_engineering_challenge.ipynb'
    result = subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', notebook_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{lab_name} - The lab notebook did not run with error \n {result.stderr}"
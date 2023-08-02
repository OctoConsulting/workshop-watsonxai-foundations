import os, subprocess

base_directory = os.path.join(os.getcwd(), "self-guided-labs")

def test_challenge_01():
    challenge_name = "challenge 01"
    notebook_path = base_directory + '/apply-lessons-learned/challenge-01/news-article-classification.ipynb'
    result = subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', notebook_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{challenge_name} - The challenge notebook did not run with error \n {result.stderr}"
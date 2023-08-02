import nbformat, requests, re, os
from urllib.parse import urlparse


### UTIL #####

def get_urls_from_text(txt):
    endpoints = {"https://us-south.ml.cloud.ibm.com"}
    url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    urls = re.findall(url_regex, txt)
    urls = [url if url[-1]!=')' else url[:-1] for url in urls]
    urls = [url for url in urls if url not in endpoints]
    return urls


def get_links_from_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    links = []
    for cell in notebook.cells:
        if cell.cell_type == 'markdown':
            urls = get_urls_from_text(cell.source)
            links += urls

    return links

def get_links_from_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        urls = urls = get_urls_from_text(content)
        return urls


base_directory = os.path.join(os.getcwd(), "self-guided-labs")

def assert_links_200(links, file_path):
    for link in links:
        if urlparse(link).scheme in ('http', 'https'):
            response = requests.head(link, allow_redirects=True)
            assert response.status_code == 200, f"Link {link} in {file_path} returned status code {response.status_code}"

#### TESTS #####

def test_links_lab02():
    # readme
    md_path = base_directory + '/level-1/lab-02-advanced-prompt-engineering/README.md'
    md_links = get_links_from_markdown(md_path)
    assert_links_200(md_links, md_path)

    #notebook
    notebook_path = base_directory + '/level-1/lab-02-advanced-prompt-engineering/prompt_engineering_challenge.ipynb'
    notebook_links = get_links_from_notebook(notebook_path)
    assert_links_200(notebook_links, notebook_path)

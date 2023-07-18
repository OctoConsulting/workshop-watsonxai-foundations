# Create Virtual Python Environment
Python applications import multiple libraries, and oftentimes, conflicts can occur between different versions of required libraries.  However your app may require a specific library version due to a bug fix.  The solution is to create a virtual environment, a self-contained suite of libraries for a specific Python installation.

We will use Python's built-in virtual environment functionality, becuase as of the February 25, 2023, [Conda/Miniconda is now on IBM's "do-not-use" list](https://w3.ibm.com/w3publisher/ossc-process/exception-and-do-not-use) because of use of the Anaconda repo.

While creating your virtual Python environment below, you will also be installing all the libraries required to complete this Boot Camp including Jupyter Notebooks, Hugging Face libraries, ChromaDB and LangChain.

## Python's Built-In Virtual Environments <a id="python-virtual-environment"></a>
Python version 3.3 introduced [a built-in environments module called venv](https://docs.python.org/3/tutorial/venv.html), but few people used it until recently.  You may find using venv easier than Conda as it works directly with pip. 

#### Upgrade to Python v3.11 to Avoid Any Conflicts
Upgrading Python versions can be complicated so don't be afraid to ask for help during this process.  We have documented best practices to assist you.  You may have no issues using Python 3.8 plus, but recall that even Python 3.9 is 2.5 years old.  [Follow these best practices to upgrade to Python 3.11](upgrade-python.md).

#### Create your Python virtual environment
First create a folder where you will create and store your Python virtual environment.  Then open a terminal/console window and enter the commands below to create a Python environment called `genai`. The new virtual environment will result in a local directory by the same name.
```
cd <directory to store your Python environment>
python -m venv genai
```

#### Download requirements_venv.txt
Download [requirements_venv.txt](./requirements_venv.txt) which contains the list of initial packages to install in your environment.  Move the requirements.txt file to the folder that you created for your Python environments.

#### Activate your Python virtual environment
Execute these commands:
```
source genai/bin/activate
python -m pip install -r requirements_venv.txt
```

You can validate that your environment is active by looking at the start of the prompt line in your terminal/console window.  As shown below, the start of the prompt changes to show (genai).

<p align="left">
  <img src="images/environment-activated-python.png" width="500"/>
</p>

#### Dectivate your Python virtual environment
You deactivate your environment using the command below:
```
deactivate
```

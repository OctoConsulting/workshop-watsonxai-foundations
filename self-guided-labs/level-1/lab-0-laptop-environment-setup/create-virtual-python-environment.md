# Create Virtual Python Environment
Python applications import multiple libraries, and oftentimes, conflicts can occur between different versions of required libraries.  However your app may require a specific library version due to a bug fix.  The solution is to create a virtual environment, a self-contained suite of libraries for a specific Python installation.

You have two options for creating a virtual Python environment:
1. [Option 1: Conda environments](#conda-virtual-environment)
2. [Option 2: Python's built-in environments](#python-virtual-environment)

Choose an option based on your own personal preference after reading the docs.  While creating your virtual Python environment below, you will also be installing all the libraries required to complete this Boot Camp including Jupyter Notebooks, Hugging Face libraries, ChromaDB and LangChain.

## Option 1: Conda environments <a id="conda-virtual-environment"></a>
[Miniconda](https://conda.io/miniconda.html) is a lighweight version of Anaconda.  The full Anaconda installation has enterprise licensing requirements that preclude using it for free as an IBMer. Please install Miniconda instead.  You may want to read [learn more about Conda Environments](https://whiteboxml.com/blog/the-definitive-guide-to-python-virtual-environments-with-conda) before proceeding.

If Conda is your choice for a Python Environment Manager, then [install miniconda](https://docs.conda.io/en/latest/miniconda.html) as the remainder of this section assumes you have it installed.

#### Create virtual environment
Download [requirements_conda.txt](./requirements_conda.txt), which contains the list of initial packages to install in your environment.  Then open a terminal/console window and enter the commands below to create a Conda environment called `genai` with Python version 3.11.
```
cd <full path to folder containing downloaded requirements_conda.txt file>
conda create --name genai --file requirements_conda.txt python=3.11 --channel anaconda
```

#### requirements_conda.txt
Open the [requirements_conda.txt](./requirements_conda.txt) to view all libraries there were installed during the creation of your Conda environment such as Jupyter Notebooks, Hugging Face libraries, ChromaDB and other libraries required for this Boot Camp.

#### Activate your Conda environment
Execute this command to activate your Conda environment:
```
conda activate genai
```
You can validate that your environment is active by looking at the start of the prompt line in your terminal/console window.  As shown below, the start of the prompt changes to show (genai).

![image](./images/environment-activated-conda.png)

#### Installing libraries not in the default Conda channel
Sometimes libraries are unavailable in Conda's default installation channel.  The easiest solution for those libraries is to usu "pip" to install them. Run the following command install these additional librariestime.  If you get an error about pip not being found, replace "pip" with "pip3" in the commands below.
```
pip install -r requirements_conda_pip.txt
```

## Option 2: Python's Built-In Environments <a id="python-virtual-environment"></a>
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

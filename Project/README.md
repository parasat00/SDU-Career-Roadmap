# EXECUTION

## How to launch a project via windows?

### Check if there is a python in the computer or not

  In order to check whether there is python in our computer or not, it is necessary to write cmd in the working window in the search or press start +R and write cmd and the command line opens and write "python" or "python --version".
  
  ```
  python
  python --version
  ```
    
  If python or its version comes out, you have python installed on your PC, and if there is an error, download it on the [official website](https://www.python.org/). In the process of installing the cartridge in the optional features page, select the pip checkmark and download

### Check if there is a pip in the computer or not

  In the same command line, you should write pip or pop --version or pip -V.If it works, then the pip version or attributes are output.
  ```
  pip
  pop --version
  pip -V
  ```
  And if not, follow these guides step by step for installing pip on [Windows](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/), [Mac](https://www.geeksforgeeks.org/how-to-install-pip-in-macos/) or [ubuntu](https://www.odoo.com/ru_RU/forum/pomoshch-1/how-to-install-pip-in-python-3-on-ubuntu-18-04-167715).

### Download virtualenv

  Virtualenv is used to manage Python packages for different projects. Using virtualenv allows you to avoid installing Python packages globally which could break system tools or other projects. You can install virtualenv using pip.
  To install virtualenv,you must write in command line one of these commands:
  ```
  pip install virtualenv
  pip install --user virtualenv
  py -m pip install --user virtualenv
  ```

### Clone the repository to your PC or Laptop
  Use the git clone command:
  ```
  git clone https://github.com/SuleymanDemirelKazakhstan/diploma-project-bad-boys.git
  ```

### Create virtualenv
  Creating a virtual environment virtualenv (for Python 2) allow you to manage separate package installations for different projects. They essentially allow you to create a “virtual” isolated Python installation and install packages into that virtual installation. When you switch projects, you can simply create a new virtual environment and not have to worry about breaking the packages installed in the other environments. It is always recommended to use a virtual environment while developing Python applications.
  To create a virtual environment, cd to your project’s directory and run one of these commands:
  ```
  virtualenv <my_env_name>
  python -m virtualenv <my_env_name>
  ```
### Activating a virtual environment
  To activate a virtual environment:
  ```
  <env_name>\Scripts\activate
  ```
  If you want to deactivate virtualenv use this command:
  ```
  deactivate
  <env_name>\Scripts\deactivate  (in some cases)
  ```


### How to install package using the ip command inside settings.txt

  Find the location where the settings.txt is located at and cd there. After run this command:
  ```
  pip install -r requirements.txt
  ```


### Run the project

  Check that the project is starting. To do this, cd to the location where manage.py is, then run this python command: 
  ```
  python manage.py runserver
  ```
  If everything is configured correctly, you should see the message Starting development server at http://127.0.0.1:8000/
  Copy and paste this url in the browser tab. Enjoy :)

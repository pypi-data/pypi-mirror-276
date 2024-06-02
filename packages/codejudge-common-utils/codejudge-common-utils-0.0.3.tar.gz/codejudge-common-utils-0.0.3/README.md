CODEJUDGE COMMON UTIL


TESTING
    Whenever any changes are made in this module, follow the steps mentioned below:

        If changes are made in setup.py file:
            Run this command "python setup.py sdist bdist_wheel" in the terminal to check for any error

        a. Push the changes to master
        b. Run "git log" in terminal and copy the latest commit id and place it in requirements.txt of other repos
        c. Delete common package and codejudge_common_utils-0.0.1.dist-info folder from venv in the other repo
        d. Run "pip install -r requirements.txt" to reinstall the library in other repos to apply the latest changes

    To test locally, follow the steps mentioned below:
        a. Run this command "python setup.py sdist bdist_wheel" in the terminal
        b. Following folders will be created
            - dist
            - build
            - codejudge_common_util-0.0.1.dist-info
        c. Delete common package and codejudge_common_utils-0.0.1.dist-info folder from venv in the other repo
        d. Run the below command in the other repo where you want to install 
            Replace the path with your path to codejudge-common-util
            "python -m pip install /Users/yash/Desktop/Codejudge/codejudge-common-util/dist/codejudge-common-utils-0.0.1.tar.gz"


ISSUES AND FIXES
    If facing issue in installing library or in running the command, take reference from the mentioned link:- https://docs.djangoproject.com/en/5.0/intro/reusable-apps/

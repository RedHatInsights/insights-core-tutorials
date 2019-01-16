#!/bin/sh

# Make sure git, gcc and python3.6 are installed.
is_installed() {

    echo ''
    echo '*** Making sure git and gcc are installed ***'

    pckarr=(git gcc)
    for i in  ${pckarr[*]}
     do
       if yum list installed $i >/dev/null 2>&1;
       then
        echo $i is installed
      else
        echo $i is not INSTALLED!!!!
        echo To install, run this command as root: yum install $i
        exit 1
      fi
    done
}

# Check if Python3.6 is installed
is_python36() {

    echo ''
    echo '*** Making sure python3.6 is installed ***'

    if command -v python3.6 &>/dev/null; then
        echo Python 3.6 is installed
    else
        echo Python 3 is not installed
        echo To install, run this command as root: yum install python36
        exit 1
    fi
}

# Setup the python virtual environment
setup_environment(){

    echo ''
    echo '*** Setting up the development environment ***'

    if ! command -v ./bin/python3.6 &>/dev/null; then
           virtualenv -p python3.6 .
    else
        echo virtualenv already set up.
    fi

    # Activate the python virtual environment
    source ./bin/activate

    # Make sure we have the most recent version of pip
    pip install --upgrade pip

    # Install tutorials to to the virtual environment
    pip install -e .[develop]
}

# Create the 'mycomponents' directory structure
create_mycomponents_dirs(){

    echo ''
    echo '*** Creating the mycomponents directories ***'

    mkdir -p ./mycomponents/parsers/tests
    touch ./mycomponents/__init__.py
    touch ./mycomponents/parsers/__init__.py
    touch ./mycomponents/parsers/tests/__init__.py
    mkdir -p ./mycomponents/combiners/tests
    touch ./mycomponents/combiners/__init__.py
    touch ./mycomponents/combiners/tests/__init__.py
    mkdir -p ./mycomponents/rules/tests
    touch ./mycomponents/rules/__init__.py
    touch ./mycomponents/rules/tests/__init__.py
}

# Run pytest
run_pytest() {

    echo ''
    echo '*** Running pytest ***'

    pytest
}

is_installed
is_python36
setup_environment
create_mycomponents_dirs
run_pytest


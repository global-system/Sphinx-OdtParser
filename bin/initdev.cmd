call %~dp0\..\config\sethome.cmd 

%PYTHON_HOME%\python -m venv %~dp0\..\venv

set path=%~dp0\..\venv\Scripts;%path%

python -m pip install --upgrade pip
python -m pip install sphinx
python -m pip install sphinx-autobuild
python -m pip install sphinx-rtd-theme
python -m pip install panflute

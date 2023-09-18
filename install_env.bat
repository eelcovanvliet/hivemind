REM inplace environment creation
REM =======================================
call conda remove --prefix ./.venv --all -y
call conda create --prefix ./.venv -y
call activate ./.venv
call conda install pip -y
call pip install -e .[testing]

cmd /k
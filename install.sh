echo "Installing Dependencies";
sudo apt-get install python-dev libmysqlclient-dev
sudo apt-get install python-mysqldb
cp config.sample config.py
mkdir logs
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
sudo apt-get install python-virtualenv && virtualenv --system-site-packages env && (env/bin/pip install setuptools &&
env/bin/pip install -r requirements.txt)
echo "Dependencies Installed";
echo "Its a good idea to run tests now :)";


activate_this = '/usr/lib/online_store/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.append('/usr/lib/online_store')
from src.app import app as application
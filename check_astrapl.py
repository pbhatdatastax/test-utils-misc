# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck
from datadog_checks.base.utils.subprocess_output import get_subprocess_output
import datetime
import time
import os

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class astraplCheck(AgentCheck):
    def check(self, instance):
        t0 = datetime.datetime.now()
        token = os.environ['ASTRA_TOKEN']
        cluster = os.environ['dbID']
        try:
            out, err, retcode = get_subprocess_output(["/opt/datadog-agent/cqlsh_command.sh", "-t", token, "-b", "/opt/datadog-agent/scb.zip", "-c", cluster], self.log, raise_on_empty_output=True) 
        except Exception as ex:
            self.log.exception("Error collecting cqlstats:", ex)
        t1 = datetime.datetime.now()
        td = t1 - t0
        out = int(out)
        tags_env = 'clusterid:' + cluster
#        self.gauge('astra.synth.pldelay', td.microseconds, tags=['service:privatelink',tags_env] + self.instance.get('tags', []) )
        self.gauge('astra.synth.avail', out, tags=['service:privatelink', tags_env] + self.instance.get('tags', []) )


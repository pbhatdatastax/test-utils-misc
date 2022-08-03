
#test out AWS lambda connectivity to PrivateLink endpoint
#which can be run by customer on AWS lambda.
#output will be in Lambda "execution results" tab or in cloudwatch logs.
import socket
import logging
import ssl
#ASTRA DB URL , Replace with correct ASTRA DB URL.
REMOTE_SERVER = "7e4cf49f-1965-4bbe-9744-XXXXXSAAA-us-west-2.db.astra.datastax.com"
#ASTRA DB METADATA PORT
WEBPORT=29080
#ASTRA DB CQL PORT
CQLPORT=29042

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
def lambda_handler(event, context):
  try:
    host = socket.gethostbyname(REMOTE_SERVER)
    logger.debug('## Hostname Resolution')
    logger.debug(host)
  except Exception:
    logger.debug("Hostname resolution failed")
  
  try:
    # connect to the host -- tells us if the host is actually reachable
    s = socket.create_connection((host, WEBPORT), 2)
    logger.debug(s)
    s.close()
  except Exception:
     # we ignore any errors, returning False
     logger.debug("Connection to host ip %s and metadata port %s Failed", host, WEBPORT)  
  
  try:
    cert = ssl.get_server_certificate((REMOTE_SERVER,WEBPORT),ssl_version=2)
    logger.debug("certificate from host IP %s and metadata port %s", REMOTE_SERVER, WEBPORT)
    logger.debug(cert)
  except Exception:
    logger.debug("Could not get any certificate from host %s and metadata port %s Failed", REMOTE_SERVER, WEBPORT)  
    
  try:
    cert = ssl.get_server_certificate((REMOTE_SERVER,CQLPORT),ssl_version=2)
    logger.debug("certificate from host %s and CQL port %s", REMOTE_SERVER, CQLPORT)
    logger.debug(cert)
  except Exception:
    logger.debug("Could not get any certificate from host IP %s and CQL port %s Failed", host, CQLPORT)  
    
  return

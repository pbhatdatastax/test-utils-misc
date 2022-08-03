import socket
import logging
import ssl
REMOTE_SERVER = "7e4cf49f-1965-4bbe-9744-5779c4acc0eb-us-west-2.db.astra.datastax.com"
WEBPORT=29080
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
     logger.debug("Connection to host IP %s and metadata port %s Failed", host, WEBPORT)  
  
  try:
    cert = ssl.get_server_certificate((host,WEBPORT),ssl_version=2)
    logger.debug("certificate from host IP %s and metadata port %s", host, WEBPORT)
    logger.debug(cert)
  except Exception:
    logger.debug("Could not get any certificate from host IP %s and metadata port %s Failed", host, WEBPORT)  
    
  try:
    cert = ssl.get_server_certificate((host,CQLPORT),ssl_version=2)
    logger.debug("certificate from host IP %s and CQL port %s", host, CQLPORT)
    logger.debug(cert)
  except Exception:
    logger.debug("Could not get any certificate from host IP %s and CQL port %s Failed", host, CQLPORT)  
    
  return

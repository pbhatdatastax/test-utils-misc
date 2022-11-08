 # syntax=docker/dockerfile:1
FROM gcr.io/datadoghq/agent:7

COPY cqlsh_command.sh  /opt/datadog-agent/.
COPY check_astrapl.py /etc/datadog-agent/checks.d/.
COPY check_astrapl.yaml /etc/datadog-agent/conf.d/.

# install jq to parse json within bash scripts
RUN apt-get -y -qq update && apt-get -y -qq install jq

RUN curl -SL https://downloads.datastax.com/enterprise/cqlsh-astra.tar.gz -o /opt/datadog-agent/cqlsh-astra.tar.gz
RUN tar -xzf /opt/datadog-agent/cqlsh-astra.tar.gz -C /opt/datadog-agent/
RUN chmod +x  /opt/datadog-agent/cqlsh_command.sh


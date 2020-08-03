FROM docker.elastic.co/kibana/kibana-oss:7.6.2
RUN kibana-plugin install https://github.com/johtani/analyze-api-ui-plugin/releases/download/7.6.2/analyze_api_ui-7.6.2.zip
RUN kibana --optimize

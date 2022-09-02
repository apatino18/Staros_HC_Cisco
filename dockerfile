# Python Image
FROM python

# Create working Folder
RUN mkdir /healthcheck/

# Copy Health Check Files to container:
#   Testbed.xlsx 
#   HC_ASR.py
#   testcase
COPY HC_FILES/ /healthcheck/

# Download latest version of pyats
RUN pip install pyats[full]

# Clone Genie Parsers
RUN cd /healthcheck/ && git clone https://github.com/CiscoTestAutomation/genieparser.git

# Create StarOS parser folder
RUN cd /healthcheck/genieparser/src/genie/libs/parser/ && mkdir staros/

#Copy StarOS parsers to container
COPY staros/ /healthcheck/genieparser/src/genie/libs/parser/staros/

# Add New parsers to Pyats
RUN cd /healthcheck/genieparser/ && make develop && make json
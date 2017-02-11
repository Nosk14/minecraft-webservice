FROM frolvlad/alpine-python3
COPY requirements.txt .
RUN pip3 install -r requirements.txt --upgrade
COPY src /usr/local/minecraft-webservice/
CMD python3 /usr/local/minecraft-webservice/start.py
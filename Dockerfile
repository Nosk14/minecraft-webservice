FROM frolvlad/alpine-python3
COPY requirements.txt .
RUN pip3 install -r requirements.txt --upgrade
COPY src /usr/local/engendro-bot/
CMD python3 /usr/local/engendro-bot/main.py
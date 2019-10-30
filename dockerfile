FROM python

WORKDIR "~/Dockerfiles/proctoring/proctoring/"

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]

CMD["proctoring/config/wsgi.py"]

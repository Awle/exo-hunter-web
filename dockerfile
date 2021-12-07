FROM python:3.8-buster

RUN apt update
RUN apt install -y libcairo2-dev libpango1.0-dev ffmpeg
RUN pip install -U pip

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY exo-hunter-web /exo-hunter-web
COPY website.py /website.py
COPY data /data
COPY animation.py /animation.py

#EXPOSE $PORT
#ENTRYPOINT ["streamlit", "run"]
CMD streamlit run website.py --server.port $PORT

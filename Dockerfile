FROM python:3.6.8
COPY src /src
RUN mkdir /audios
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --upgrade pip
RUN pip install pandas
RUN pip install beautifulsoup4
RUN pip install pymongo
RUN pip install requests
RUN pip install -U youtube_dl
ENV PYTHONUNBUFFERED=1
CMD python src/main.py

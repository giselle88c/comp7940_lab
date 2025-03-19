FROM python:3.10
WORKDIR /APP
COPY . /APP
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "chatbot.py"]
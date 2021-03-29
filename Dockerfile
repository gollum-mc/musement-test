FROM python:3.8-slim-buster
WORKDIR /code
ENV PYTHONPATH .
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "app/main.py"]
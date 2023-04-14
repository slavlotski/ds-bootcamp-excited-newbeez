FROM python:3.9.6-slim
WORKDIR /app


COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt && pip cache purge
COPY . ./
CMD python bot.py


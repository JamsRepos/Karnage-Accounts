FROM tiangolo/meinheld-gunicorn:python3.8
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./app/bot.py" ]
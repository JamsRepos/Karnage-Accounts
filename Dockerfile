FROM tiangolo/meinheld-gunicorn:python3.8
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app
CMD [ "python", "/app/bot.py" ]
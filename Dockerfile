FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir Flask python-dotenv gevent
EXPOSE 5000
ENV STAGE=PROD
ENV PORT=5000

CMD ["python", "main.py"]
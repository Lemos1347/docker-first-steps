FROM python:3.11.2


WORKDIR /backend


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 3001


CMD [ "python", "app.py"]
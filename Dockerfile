FROM python:3.8-slim-buster

WORKDIR /A_DONOR_WEB_APP

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install torch==1.9.0+cpu torchvision==0.10.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

COPY . .

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]
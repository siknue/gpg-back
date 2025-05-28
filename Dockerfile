FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt ./
COPY app ./app
COPY .env ./.env

RUN pip install -r ./requirements.txt

CMD ["app.main.handler"]
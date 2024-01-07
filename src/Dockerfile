FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

COPY main.py cmdict_bot/ ${LAMBDA_TASK_ROOT}

RUN python ${LAMBDA_TASK_ROOT}/cmdict_bot/db.py

CMD [ "main.handler" ]

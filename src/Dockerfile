FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt ${LAMBDA_TASK_ROOT}/

RUN pip install -r requirements.txt

COPY cmdict_bot/ ${LAMBDA_TASK_ROOT}/cmdict_bot/

COPY main.py __init__.py ${LAMBDA_TASK_ROOT}/

RUN python -m cmdict download

ENV CMDICT_HISTORY="value does not matter"

CMD [ "main.lambda_handler" ]

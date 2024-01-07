FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt ${LAMBDA_TASK_ROOT}/

RUN pip install -r requirements.txt

COPY cmdict_bot/ ${LAMBDA_TASK_ROOT}/cmdict_bot/

COPY main.py __init__.py set_up_db.py ${LAMBDA_TASK_ROOT}/

RUN python -m cmdict download

CMD [ "main.handler" ]

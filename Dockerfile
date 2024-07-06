# The builder image, used to build the virtual environment
FROM python:3.11-slim as builder

#RUN apt-get install gcc
#RUN apk update && apk add gcc libc-dev libffi-dev
RUN pip install --upgrade pip && pip install poetry==1.7.1

RUN which poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN ls -la /usr/local/bin

WORKDIR /ct-iot-user-service

COPY pyproject.toml poetry.lock requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt
#RUN touch README.md

#RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR


# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim as runtime

COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ENV VIRTUAL_ENV=/ct-iot-user-service/venv \
    PATH="/usr/local/bin:/ct-iot-user-service/venv/bin:$PATH"

WORKDIR /ct-iot-user-service

ENV PYTHONPATH src/

COPY . .

RUN ls -la

CMD ["uvicorn", "user_service.service:server", "--port", "8001"]

EXPOSE 8001
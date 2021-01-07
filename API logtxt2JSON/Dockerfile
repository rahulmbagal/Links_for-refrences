From python:latest
COPY . /app
WORKDIR /app

RUN pip install -r requirement.txt
ENV PORT 8080


ENTRYPOINT ["python"]
CMD ["run.py"]

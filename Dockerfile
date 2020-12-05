# https://cloud.google.com/cloud-build/docs/quickstart-build
FROM Alpine
COPY main.py /
CMD ["python3 main.py"]

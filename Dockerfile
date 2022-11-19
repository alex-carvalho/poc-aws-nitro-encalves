FROM python:3.7.9-alpine3.12

COPY enclave.py .

CMD ["/usr/local/bin/python3", "enclave.py"]
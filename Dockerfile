FROM python:3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /root/clove
WORKDIR /root/clove

CMD ["/bin/bash"]

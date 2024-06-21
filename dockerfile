FROM python
RUN adduser app
COPY requirements.txt /home/app
RUN pip install -r /home/app/requirements.txt
COPY . /home/app
RUN echo "#!/bin/bash">>/bin/run.sh
RUN cat /home/app/scripts/NAME>>/bin/run.sh
RUN chmod +x /bin/run.sh
RUN pip install /home/app && rm -rf /home/app/*
USER app
CMD ["/bin/run.sh"]

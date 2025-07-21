FROM python
RUN adduser app
COPY requirements.txt /home/app
RUN pip install -r /home/app/requirements.txt
COPY . /home/app
RUN echo "#!/bin/bash">>/bin/entrypoint.sh
RUN cat /home/app/scripts/NAME >> /bin/entrypoint.sh
RUN echo "_web" >>/bin/entrypoint.sh
RUN chmod +x /bin/entrypoint.sh
RUN pip install /home/app && rm -rf /home/app/*
CMD ["/bin/entrypoint.sh"]

FROM python
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN echo "#!/bin/bash">>/bin/run.sh
RUN cat scripts/NAME>>/bin/run.sh
RUN chmod +x /bin/run.sh
RUN pip install .
CMD ["/bin/run.sh"]

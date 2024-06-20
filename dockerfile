FROM python
COPY . .
RUN pip install .
CMD ["my_app"]

FROM python:3.8

RUN pip install --upgrade pip

# Setup application
COPY ./ /app
RUN chmod +x /app/scripts/*.sh
WORKDIR /app/

# Install application
RUN pip install -r requirements.txt

ARG INSTALL_EXTRAS=''
RUN pip install /app$INSTALL_EXTRAS

# Start
EXPOSE 80
CMD ["/app/scripts/start.sh"]

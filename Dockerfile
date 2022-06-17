# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim
WORKDIR /app
ENV FLASK_APP app.py
COPY requeriments.txt requeriments.txt
RUN pip install -r requeriments.txt
COPY . /app
EXPOSE 5000
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python","-m","flask", "run", "--host=0.0.0.0"]

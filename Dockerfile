FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml requirements.txt ./
COPY src ./src
COPY evaluation ./evaluation
RUN pip install --no-cache-dir . && mkdir /app/reports && chown 65532:65532 /app/reports
USER 65532:65532
ENTRYPOINT ["python", "-m", "agro_conecta_iot"]
CMD ["simulate", "--scenario", "normal", "--dry-run"]

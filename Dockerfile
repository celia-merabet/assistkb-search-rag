FROM python:3.10

WORKDIR /app

# Étape 1 : torch CPU seul (le plus gros, 190 MB)
RUN pip install --no-cache-dir --timeout 120 --retries 10 \
    --extra-index-url https://download.pytorch.org/whl/cpu torch==2.3.1+cpu

# Étape 2 : les paquets scientifiques lourds
RUN pip install --no-cache-dir --timeout 120 --retries 10 \
    numpy==1.26.4 scipy scikit-learn

# Étape 3 : le reste (léger)
RUN pip install --no-cache-dir --timeout 120 --retries 10 \
    qdrant-client==1.9.1 sentence-transformers==2.7.0 fastapi==0.110.0 \
    uvicorn==0.27.1 beautifulsoup4==4.12.3 lxml==5.1.0 pypdf==4.2.0 \
    tqdm==4.66.2 langdetect==1.0.9 requests==2.31.0

# Le code en DERNIER : modifier le code ne re-déclenche plus les pip install
COPY . .

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
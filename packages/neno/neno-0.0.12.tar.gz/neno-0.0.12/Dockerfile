FROM jupyter/scipy-notebook@sha256:fca4bcc9cbd49d9a15e0e4df6c666adf17776c950da9fa94a4f0a045d5c4ad33

# global pip cache, to speed up venv setup
RUN echo "[global]\ndownload_cache = ~/.pip/cache" >> $HOME/.pip/pip.conf 

RUN pip install "neno[server]"==0.0.11

WORKDIR /etc/neno
COPY src/neno/config.yaml .

ENTRYPOINT [ "python", "-m", "neno" ]

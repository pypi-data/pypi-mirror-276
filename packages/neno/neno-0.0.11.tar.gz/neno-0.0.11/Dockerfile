FROM jupyter/scipy-notebook@sha256:fca4bcc9cbd49d9a15e0e4df6c666adf17776c950da9fa94a4f0a045d5c4ad33

# global pip cache, to speed up venv setup
RUN echo "[global]\ndownload_cache = ~/.pip/cache" >> $HOME/.pip/pip.conf 

COPY src/neno/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install -i https://test.pypi.org/simple/ neno==0.0.8

WORKDIR /etc/neno
COPY src/neno/config.yaml .

ENTRYPOINT [ "python", "-m", "neno" ]

###############################################################################
# main
###############################################################################

FROM continuumio/miniconda3:4.10.3 AS main

RUN apt-get -y --allow-releaseinfo-change update && \
    apt-get -y install build-essential
RUN conda update -n base -c defaults conda

WORKDIR /opt/app

# chown changes owner from root owner (1000) to the first user inside the env (100)
COPY --chown=1000:100 requirements.txt .
RUN conda install --force-reinstall -y -q --name base -c conda-forge --file requirements.txt

COPY src src
COPY data data

EXPOSE 8888
EXPOSE 8050

CMD python src/app.py

###############################################################################
# test
###############################################################################

FROM main AS test

COPY tests tests
RUN py.test tests

###############################################################################
# notebook
###############################################################################

FROM main as notebook

EXPOSE 8888
CMD jupyter lab \
  --ip=0.0.0.0 \
  --notebook-dir=notebooks \
  --allow-root \
  --NotebookApp.token="" \
  --NotebookApp.password=""


###############################################################################
# dashboard
###############################################################################

FROM main as dashboard

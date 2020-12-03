FROM kbase/sdkbase2:python
MAINTAINER zyang@bnl.gov
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

# RUN apt-get update


# -----------------------------------------


RUN \
    apt-get update && \
    apt-get -y install gcc
#RUN conda update --yes --force conda

RUN conda install -c conda-forge -c bioconda checkv
RUN conda install --yes -c conda-forge -c bioconda diamond=2.0.4
RUN conda install -c conda-forge -c bioconda numpy
# RUN conda install -c conda-forge -c bioconda diamond=2.0.4
#RUN pip install Jinja2
#RUN pip install nose
#RUN pip install jsonrpcbase

ENV CHECKVDB="/data/checkv-db-v0.6"
COPY ./ /kb/module

RUN mkdir -p /opt/work/outputdir && \
    mkdir -p /opt/work/checkv
RUN git clone https://bitbucket.org/berkeleylab/checkv.git /opt/work/checkv

RUN chmod -R a+rw /kb/module
RUN mkdir -p /data

WORKDIR /kb/module
RUN  make all


ENTRYPOINT [ "./scripts/entrypoint.sh"]
CMD [ ]


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

RUN pip install checkv
#RUN conda install --yes -c conda-forge -c bioconda diamond
#RUN conda install -c bioconda diamond
#RUN conda install -c conda-forge -c bioconda numpy
RUN apt-get install wget
RUN wget http://github.com/bbuchfink/diamond/releases/download/v2.0.5/diamond-linux64.tar.gz && \
    tar -zxf diamond-linux64.tar.gz diamond && \
    mv diamond /kb/deployment/bin/diamond
#ENV PATH=/kb/runtime/bin:/kb/deployment/bin:/miniconda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
#RUN which diamond
RUN apt-get install prodigal
RUN apt-get --yes install hmmer
# RUN conda install -c conda-forge -c bioconda diamond=2.0.4
#RUN conda install Jinja2
#RUN conda install nose
#RUN pip install jsonrpcbase # cannot run conda install, no version available

ENV CHECKVDB="/data/checkv-db-v0.6"
COPY ./ /kb/module

RUN mkdir -p /opt/work/outputdir && \
    mkdir -p /opt/work/checkv
RUN git clone https://bitbucket.org/berkeleylab/checkv.git /opt/work/checkv

RUN chmod -R a+rw /kb/module
RUN mkdir -p /data

WORKDIR /kb/module
RUN  make all
ENV PATH=/kb/runtime/bin:/kb/deployment/bin:/miniconda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin


ENTRYPOINT [ "./scripts/entrypoint.sh"]
CMD [ ]


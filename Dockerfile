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
RUN conda install -c conda-forge -c bioconda checkv
RUN mkdir -p /kb/module/work/outputdir && \
    mkdir -p /kb/module/work/checkv
RUN git clone https://bitbucket.org/berkeleylab/checkv.git /kb/module/work/checkv
RUN pip install numpy

RUN chmod -R a+rw /kb/module
ENV CHECKVDB="/data/checkv-db-v0.6"
COPY ./ /kb/module
RUN mkdir -p /data && \
    mkdir -p /data/checkv-db-v0.6
WORKDIR /kb/module
RUN  make all

ENTRYPOINT [ "./scripts/entrypoint.sh"]
CMD [ ]

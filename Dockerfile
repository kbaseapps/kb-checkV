FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

# RUN apt-get update


# -----------------------------------------


RUN apt-get update
RUN apt-get -y install gcc
RUN conda install -c conda-forge -c bioconda checkv
RUN mkdir -p /kb/module/work/database
RUN checkv download_database /kb/module/work/database
RUN git clone https://bitbucket.org/berkeleylab/checkv.git /kb/module/work/checkv
ENV CHECKVDB="/kb/module/work/database/checkv-db-v0.6"
COPY ./ /kb/module
RUN mkdir -p /kb/module/work/outputdir

# RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]

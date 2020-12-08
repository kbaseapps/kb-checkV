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
#
# RUN apt-get install  -y apt-transport-https ca-certificates gnupg software-properties-common wget \
#     libc6 \
#     libgcc-s1 \
#     libssl1.1 \
#     libstdc++6
# RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | sudo tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null && \
#     apt-add-repository 'deb https://apt.kitware.com/ubuntu/ focal main' && \
#     apt-get update && \
#     apt-get install -y cmake
RUN apt-get install wget
RUN apt-get install --yes cmake
RUN apt-get install --yes build-essential
RUN apt-get install --yes zlib1g-dev
RUN wget http://github.com/bbuchfink/diamond/archive/v2.0.4.tar.gz && \
    tar xzf v2.0.4.tar.gz && \
    cd diamond-2.0.4 && \
    mkdir bin && \
    cd bin && \
#     cmake -DCMAKE_INSTALL_PREFIX=/kb/deployment/bin && \
#     cmake -DCMAKE_BUILD_MARCH=nocona
    cmake -DCMAKE_BUILD_MARCH=native .. && \
#     cmake .. && \
    make -j4 && \
    make install
#ENV PATH=/kb/runtime/bin:/kb/deployment/bin:/miniconda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
#RUN which diamond
RUN apt-get install prodigal
RUN apt-get --yes install hmmer
# RUN conda install -c conda-forge -c bioconda diamond=2.0.4

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


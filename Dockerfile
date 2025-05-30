FROM ubuntu:18.04
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && apt-get -y install --no-install-recommends g++ clang python3 cmake libboost-dev libboost-context-dev doxygen gfortran make perl python3-pip
RUN apt-get update && apt-get install -y vim

RUN mkdir /root/simgrid_inst
RUN mkdir /root/simgrid_inst/simgrid-v3.18
WORKDIR /root/simgrid_inst/simgrid-v3.18
COPY ./simgrid-v3.18/ /root/simgrid_inst/simgrid-v3.18/

RUN cmake -DCMAKE_INSTALL_PREFIX=/opt/simgrid .
RUN make -j8
RUN make install
RUN pip3 install --upgrade pip setuptools

RUN pip3 install networkx numpy matplotlib

ENV PATH /opt/simgrid/bin/:$PATH
WORKDIR /root/workspace

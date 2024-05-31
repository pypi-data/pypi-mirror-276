# dwd4cast: a minimal python interface to load and read GRIB weather forecast data from the german weather services (DWD)

## Installation
Installing `dwd4cast`from pypi (e.g. with `pip`):
```bash
pip install dwd4cast
```
### Install binary dependencies

In order to read GRIB files the packages cfgrib is used, which depends on the [eccodes](https://github.com/ecmwf/eccodes)-library.
This can either be installed via conda:
```bash
conda create -n pythone=3.11 eccodes=2.35.0
```

or build from source. First the compression library libaec has to be present. Here we compile this also from source:
```bash
export AEC_VERSION=1.1.3
cd /tmp
curl -L https://github.com/MathisRosenhauer/libaec/releases/download/v${AEC_VERSION}/libaec-${AEC_VERSION}.tar.gz | tar xz \
    && cd libaec-${AEC_VERSION}  \
    && mkdir build && cd build \
    && ../configure \
    && make check install \
    && cd /tmp && rm -rf libaec-${AEC_VERSION}
```
    
then we compile eccodes itself:

```bash
export ECCODES_VERSION=2.35.0
export ECCODES_URL=https://confluence.ecmwf.int/download/attachments/45757960/eccodes-2.35.0-Source.tar.gz?api=v2
cd /tmp
curl ${ECCODES_URL} | tar xz \
    && mkdir eccodes-build && cd eccodes-build \
    && cmake ../eccodes-${ECCODES_VERSION}-Source \
    && make && ctest \
    && make install \
    && cd /tmp && rm -rf eccodes-*
```
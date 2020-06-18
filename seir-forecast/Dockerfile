FROM python:3.8-slim-buster

#############
## R stuff ##
## see: https://github.com/ImperialCollegeLondon/covid19model/blob/v6.0/docker/Dockerfile

## very well may be that we don't need most of this
## but just want to get the thing running first
## and later can strip down and minimize the image

RUN apt-get update 
#RUN apt-get install -y build-essential libxml2-dev libcurl4-openssl-dev libssl-dev
RUN apt-get install -y r-base
RUN apt-get install -y \
	r-cran-rstan \
	r-cran-lubridate r-cran-dplyr r-cran-matrixstats r-cran-scales r-cran-gridextra \
	r-cran-bayesplot r-cran-ggplot2 r-cran-tidyr r-cran-gdata \
	r-cran-svglite r-cran-jsonlite r-cran-optparse \
	fonts-open-sans \
	fonts-arkpandora \
	fonts-adf-verana

# failed here 
# RUN apt-get install -y r-cran-ggpubr
# testing this ..
RUN Rscript -e "install.packages('ggpubr', dependencies=TRUE)"

RUN apt-get install -y r-cran-nortest

# RUN apt-get install -y r-cran-cowplot
RUN Rscript -e "install.packages('cowplot', dependencies=TRUE)"

RUN apt-get install -y r-cran-bh

# failed here -> "install2.r: not found"
# RUN install2.r --error --deps FALSE \
# 	EnvStats BH ggplot2 isoband \
#	&& rm -rf /tmp/downloaded_packages/ /tmp/*.rds

RUN Rscript -e "install.packages(c('EnvStats', 'BH', 'ggplot2', 'isoband'), dependencies=FALSE)"
RUN rm -rf /tmp/downloaded_packages/ /tmp/*.rds

RUN Rscript -e "update.packages(.libPaths()[1])"

# WORKDIR /covid19-notebooks/bayes-by-county/

# is this redundant?
# failed here

# RUN pwd
# RUN ls
# RUN ls /

# check
ADD . .

COPY /covid19-notebooks/bayes-by-county/modelInput /covid19-notebooks/bayes-by-county/modelInput/
COPY /covid19-notebooks/bayes-by-county/stan /covid19-notebooks/bayes-by-county/stan/
COPY /covid19-notebooks/bayes-by-county/r /covid19-notebooks/bayes-by-county/r/
COPY /covid19-notebooks/bayes-by-county/py /covid19-notebooks/bayes-by-county/py/
COPY /covid19-notebooks/bayes-by-county/run.sh /covid19-notebooks/bayes-by-county/run.sh

# probably not necessary
# WORKDIR /

########
########

RUN pip3 install --upgrade pip==20.0.*
RUN pip3 install awscli==1.18.*
# WORKDIR /seir-forecast

COPY /seir-forecast/requirements.txt /seir-forecast/requirements.txt
RUN pip3 install -r /seir-forecast/requirements.txt

COPY /seir-forecast/seir-forecast.ipynb /seir-forecast/seir-forecast.ipynb
COPY /seir-forecast/run_seir_forecast.sh /seir-forecast/run_seir_forecast.sh

CMD [ "bash", "/seir-forecast/run_seir_forecast.sh" ]

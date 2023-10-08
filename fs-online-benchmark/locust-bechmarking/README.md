### Installation
This tests uses locust framework for load testing. To install the necessary depedencies you can either install it a virtual environment like conda, or use docker.

#### Standlone or single process

- Create a new conda environment `conda create -n locust python=3.11` and activate it `conda activate locust`
- Install the packages, `pip3 install -r requirements.txt`  

#### Distributed

- To run locust in distributed mode we need docker installed along with docker compose plugin. One option to install docker, if not already, is to use its convinience script https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script

- Steps to install docker image with dependencies
	
  1.  `wget https://repo.hops.works/dev/dhananjay/locust_onlinebench.tar.gz`
  2.  `docker load < locust_onlinebench.tar.gz`

### Hopsworks locust framework
The locust framework Hopsworks Feature Store can be found on [git repo](https://github.com/logicalclocks/feature-store-api/tree/master/locust_benchmark).

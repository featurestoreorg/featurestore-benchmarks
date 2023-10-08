
### Authentication

Create AWS access and secret keys for user.

### Create data

Create feature group and add data.

### Edit aws_configuration.json
1. Set access and secret key, region
2. Set feature group name
3. Set maximum number of rows in feature group and batch size for read

### Edit locustfile

Add or remove test as needed.

### Installation
If the locust environment or docker is not installed already follow the main page [README](./../README.md)

### Single process run

1. `cd aws-benchmarking`
2. `locust --headless -f locustfile_aws.py  -u 1 -s 1 -t 10 --html result.html`

### Distributed Docker run

1. `cd aws-benchmarking`

2.  Modify the `docker-compose-aws.yml` :

-  `-u`: number of users

-  `-expect-workers`: number of workers

-  `-t`: test duration

-  `-r`: users spawn rate per second

4. By default the current directory is mounted to docker container. Modify the mounted directory to make it writable for docker user as docker will write the result in this directory. Otherwise it may throw permission errors while writing the report file.

2. `docker compose -f docker-compose-aws.yml up --scale worker=4`


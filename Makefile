# ipam-o-nator make file


hubusername=chris17453
youremail=chris17453@gmail.com
image_name=wattle
image_version=latest
# openshift token
os_toklen=<xyz>
os_server=https://openshift_server.com
app_hostname=wattle.website.com

.DEFAULT: help
.PHONY: all test clean profile

help:
	@echo "wattle"
	@echo ""
	@echo "[Execute]"    
	@echo "  run              | run the container"
	@echo "  stop             | stop the container"
	@echo "  delete           | stop and delete container"
	@echo "  status           | show the status of the container"
	@echo "  debug            | run the project in local mode, no container"
	@echo "[Deploy]"    
	
	@echo "[Docker-Registry]"    
	@echo "  login            | login to a docker registry"
	@echo "  push             | push the image to a docker registry"

	@echo "[OpenShift]"    
	@echo "  openshift-new    | create a new pod in openshift"
	@echo "  openshift-update | update a pod in openshift"

	@echo "[VMWARE]"    
	@echo "  vmware-new       | create a new vm in vmware"
	@echo "  vmware-update    | update a in vmware"


	@echo "[Build]"
	@echo "  build            | build the container used to host this webui"
	@echo "  build-proxy      | build the container used to host this webui from behind a proxy"
	@echo "  export           | export the docker image to a tar for manual tranport"
	
	
	
	@echo ""
	

## BUILD
build-proxy:
	@docker build -f ./deployment/Dockerfile --build-arg http_proxy=http://172.17.0.1:3128 --build-arg https_proxy=http://172.17.0.1:3128 -t $(image_name):$(image_version) .

build:
	@docker build -f ./deployment/Dockerfile  -t $(image_name):$(image_version) .


## EXECUTE
run:
	@docker run -p 8080:8080 -u 112233 $(image_name):$(image_version)

stop:
	@echo "TO DO"

delete:
	@echo "TO DO"

status:
	@echo "TO DO"

debug:
	@python -m wattle.wsgi


## DEPLOY
export:
	@docker save --output $(image_name).$(image_version).tar $(image_name):$(image_version)

login:
	@docker login --username=$(hubusername) --email=$(youremail)

push:
	@docker tag $(docker images | grep ^$(image_name) |awk '{print $3}') $(hubusername)/$(image_name):$(image_version)
	@docker push $(hubusername)/$(image_name):$(image_version)

openshift-new:
	@oc login $(os_server)--token=$(os_token)
	@oc new-app $(hubusername)/$(image_name)
	@oc create route edge --service=$(image_name) --hostname=$(app_hostname) --port=8080-tcp

openshift-update:
	@oc import-image $(image_name):$(image_version) --from=$(hubusername)/$(image_name) --confirm


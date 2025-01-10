IMAGE_TAG ?= quay.io/cfchase/llm-eval-service:latest

build:
	podman build --platform linux/amd64 -t ${IMAGE_TAG} -f docker/Dockerfile .

push:
	podman push ${IMAGE_TAG}

run:
	podman run --platform linux/amd64 -ePORT=8080 -p8080:8080 ${IMAGE_TAG}

run-local:
	python app.py

deploy:
	oc process -p PREDICTOR_HOST=${PREDICTOR_HOST} -f templates/inference-service.yaml | oc apply -f -

undeploy:
	oc process -p PREDICTOR_HOST=${PREDICTOR_HOST} -f templates/inference-service.yaml | oc delete -f -

test-local:
	curl -k -H "Content-Type: application/json" http://localhost:8080/


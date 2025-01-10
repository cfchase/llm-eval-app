IMAGE_TAG ?= quay.io/cfchase/llm-eval-service:latest

build:
	podman build --platform linux/amd64 -t ${IMAGE_TAG} -f docker/Dockerfile .

push:
	podman push ${IMAGE_TAG}

run:
	podman run --platform linux/amd64 -ePORT=8080 -p8080:8080 ${IMAGE_TAG}

run-local:
	fastapi dev app.py

test-local:
	curl -k -H "Content-Type: application/json" http://localhost:8080/


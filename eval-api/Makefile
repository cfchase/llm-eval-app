IMAGE_TAG ?= quay.io/cfchase/eval-api:latest


BASE_STORAGE_PATH = os.environ.get("BASE_STORAGE_PATH", "/tmp/photo-generator/images")

build:
	podman build --platform linux/amd64 -t ${IMAGE_TAG} -f docker/Dockerfile .

push:
	podman push ${IMAGE_TAG}

run:
	podman run --platform linux/amd64 -ePORT=8080 -p8080:8080 ${IMAGE_TAG}

run-local:
	uvicorn app.main:app --host 0.0.0.0 --port 8080 --loop asyncio --reload

test-local:
	curl -k -H "Content-Type: application/json" http://0.0.0.0:8080/api/status


import os

ROOT_DIR = "/tmp/"
WORK_DIR = "/opt/dlami/nvme/"

# Prod / Dev 상태를 정의합니다.
ENV = os.environ["ENV"]

# RayEncoder의 resource 사용량을 정의합니다.
RAY_ENCODER_ACTOR_OPTIONS = {
    "num_gpus": int(os.environ["WORKER_NUM_GPUS"]),
    "resources": {
        "WORKER": 1,
    },
}

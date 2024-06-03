import json
import requests
from pathlib import Path
import logging
from rich.progress import Progress, SpinnerColumn, TextColumn
import subprocess
import uuid
import requests
import re

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("docker").setLevel(logging.WARNING)

def remove_tensorflow_libs(file_name):
    try:
        # Open the file in read mode
        with open(file_name, "r") as file:
            lines = file.readlines()

        # Open the file in write mode
        with open(file_name, "w") as file:
            for line in lines:
                if line.startswith('tensorflow-'):
                    # Extract package name and version
                    match = re.match(r'(tensorflow-[^=]+)==(.+)', line.strip())
                    if match:
                        package_name = match.group(1)
                        version = match.group(2)

                        # Send HTTP request to PyPI
                        url = f'http://pypi.python.org/pypi/{package_name}/{version}/json'
                        response = requests.get(url)
                        
                        if response.status_code == 200:
                            data = response.json()
                            author = data.get('info', {}).get('author', '')

                            # Check if the author is 'Google Inc.'
                            if author == 'Google Inc.':
                                print(f"Removing {package_name}=={version} as it is authored by Google Inc.")
                                continue
                
                # Write the line if not removed
                file.write(line)

        print("Processed requirements file successfully.")
    except FileNotFoundError:
        print(f"{file_name} not found")
    except Exception as e:
        print(f"An error occurred: {e}")

def remove_some_libs(file_name, lib_to_be_deleted):
    try:
        # Open the file in read mode
        with open(file_name, "r") as file:
            lines = file.readlines()

        # Open the file in write mode
        with open(file_name, "w") as file:
            for line in lines:
                if lib_to_be_deleted not in line:
                    file.write(line)

        print("Successfully removed {} from {}".format(lib_to_be_deleted, file_name))
    except FileNotFoundError:
        print("{} not found".format(file_name))

def get_tensorflow_version(filename: str) -> str:
    """
    Reads a pip's requirements.txt file and returns the TensorFlow version specified in it.
    """
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('tensorflow=='):
                    # Split the line at '==' to get the package and version
                    parts = line.strip().split('==')
                    if len(parts) == 2:
                        return parts[1]
                    else:
                        return "No specific version specified"
        return None
    except FileNotFoundError:
        return "File not found"


def build_docker_image(image_tag, config_map, tag, platform="linux/amd64", port=8000,is_tensorflow = False):
    # sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
    # sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
    # apt-get clean
    # apt-get update

    docker_list = []
    docker_list.append(add_base(image_tag))
    docker_list.append(add_env("DEBIAN_FRONTEND=noninteractive"))
    docker_list.append(add_work_dir("/src"))
    docker_list.append(copy_files("rock.yaml", "/src"))
    docker_list.append(
        copy_files("{}".format(config_map["build"]["python_requirements"]), "/src")
    )
    docker_list.append(
        copy_files("{}".format(config_map["predict"].split(":")[0]), "/src")
    )
    docker_list.append(
        add_run(
            "sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list"
        )
    )
    docker_list.append(
        add_run(
            "sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list"
        )
    )
    docker_list.append(add_run("apt-get clean"))
    docker_list.append(add_run("apt update && apt-get update"))
    docker_list.append(add_env('PATH="/root/.pyenv/shims:/root/.pyenv/bin:$PATH"'))
    docker_list.append(
        add_run(
            """--mount=type=cache,target=/var/cache/apt apt-get update -qq && apt-get install -qqy --no-install-recommends \
	make \
	build-essential \
	libssl-dev \
	zlib1g-dev \
	libbz2-dev \
	libreadline-dev \
	libsqlite3-dev \
	wget \
	curl \
	llvm \
	libncurses5-dev \
	libncursesw5-dev \
	xz-utils \
	tk-dev \
	libffi-dev \
	liblzma-dev \
	git \
	ca-certificates \
	&& rm -rf /var/lib/apt/lists/*
"""
        )
    )
    docker_list.append(
        add_run(
            """curl -s -S -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash && \
	git clone https://github.com/momo-lab/pyenv-install-latest.git "$(pyenv root)"/plugins/pyenv-install-latest && \
	pyenv install-latest {} && \
	pyenv global $(pyenv install-latest --print {}) && \
	pip install "wheel<1"
""".format(
                config_map["build"]["python_version"],
                config_map["build"]["python_version"],
            )
        )
    )
    docker_list.append(add_expose(port))
    if config_map["build"]["python_requirements"]:
        remove_some_libs(config_map["build"]["python_requirements"], "tensorflow-metal")
        remove_some_libs(config_map["build"]["python_requirements"], "tensorflow-macos")
        # remove_tensorflow_libs(config_map["build"]["python_requirements"])
        docker_list.append(
            add_run(
                "pip install -r {} {}".format(
                    config_map["build"]["python_requirements"],
                    "-i https://pypi.tuna.tsinghua.edu.cn/simple",
                )
            )
        )
        if is_tensorflow:
            tf_version = get_tensorflow_version(config_map["build"]["python_requirements"])
            docker_list.append(add_run("pip install tensorflow[and-cuda]=={} -i https://pypi.tuna.tsinghua.edu.cn/simple".format(tf_version)))
        else:# install torch
            pass

        
    docker_list.append(add_run("pip install -U rockai-cli-app"))
    docker_list.append(add_cmd("rock start"))
    save_docker_file(docker_list)
    subprocess.run(
        [
            "docker",
            "build",
            "--platform",
            platform,
            "-t",
            tag,
            "-f",
            Path.cwd() / 'temp/Dockerfile',
            Path.cwd()
        ]
    )
    # subprocess.run(["docker", "run", "--rm", tag])


def build_cpu_image(image_tag, config_map, tag, platform="linux/amd64", port=8000):
    # sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
    # sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
    # apt-get clean
    # apt-get update

    docker_list = []
    docker_list.append(add_base(image_tag))
    docker_list.append(add_env("DEBIAN_FRONTEND=noninteractive"))
    # docker_list.append(add_run("apt update && apt-get update"))
    docker_list.append(add_work_dir("/src"))
    docker_list.append(copy_files("rock.yaml", "/src"))
    docker_list.append(
        copy_files("{}".format(config_map["build"]["python_requirements"]), "/src")
    )
    docker_list.append(
        copy_files("{}".format(config_map["predict"].split(":")[0]), "/src")
    )
    docker_list.append(add_expose(port))
    if config_map["build"]["python_requirements"]:
        remove_some_libs(config_map["build"]["python_requirements"], "tensorflow-metal")
        remove_some_libs(config_map["build"]["python_requirements"], "tensorflow-macos")

        docker_list.append(
            add_run(
                "pip install -r {}".format(
                    config_map["build"]["python_requirements"]
                )
            )
        )
        
    docker_list.append(add_run("pip install -U rockai-cli-app"))
    docker_list.append(add_cmd("rock start"))
    save_docker_file(docker_list)
    subprocess.run(
        [
            "docker",
            "build",
            "--platform",
            platform,
            "-t",
            tag,
            "-f",
            Path.cwd() / 'temp/Dockerfile',
            Path.cwd()
        ]
    )
    # subprocess.run(["docker", "run", "--rm", tag])

def tf_compat_matrix():
    json_data = [
        {
            "tf_version": "tensorflow-2.16.1",
            "python": "3.9-3.11",
            "cuDNN": "8.9",
            "CUDA": "12.3",
        },
        {
            "tf_version": "tensorflow-2.15.0",
            "python": "3.9-3.11",
            "cuDNN": "8.9",
            "CUDA": "12.2",
        },
        {
            "tf_version": "tensorflow-2.14.0",
            "python": "3.9-3.11",
            "cuDNN": "8.7",
            "CUDA": "11.8",
        },
        {
            "tf_version": "tensorflow-2.13.0",
            "python": "3.8-3.11",
            "cuDNN": "8.6",
            "CUDA": "11.8",
        },
        {
            "tf_version": "tensorflow-2.12.0",
            "python": "3.8-3.11",
            "cuDNN": "8.6",
            "CUDA": "11.8",
        },
        {
            "tf_version": "tensorflow-2.11.0",
            "python": "3.7-3.10",
            "cuDNN": "8.1",
            "CUDA": "11.2",
        },
        {
            "tf_version": "tensorflow-2.10.0",
            "python": "3.7-3.10",
            "cuDNN": "8.1",
            "CUDA": "11.2",
        },
        {
            "tf_version": "tensorflow-2.9.0",
            "python": "3.7-3.10",
            "cuDNN": "8.1",
            "CUDA": "11.2",
        },
        {
            "tf_version": "tensorflow-2.8.0",
            "python": "3.7-3.10",
            "cuDNN": "8.1",
            "CUDA": "11.2",
        },
        {
            "tf_version": "tensorflow-2.7.0",
            "python": "3.7-3.9",
            "cuDNN": "8.1",
            "CUDA": "11.2",
        },
        {
            "tf_version": "tensorflow-2.6.0",
            "python": "3.6-3.9",
            "cuDNN": "8.1",
            "CUDA": "11.2",
        },
        {
            "tf_version": "tensorflow-2.5.0",
            "python": "3.6-3.9",
            "cuDNN": "8.1",
            "CUDA": "11.2",
        },
        {
            "tf_version": "tensorflow-2.4.0",
            "python": "3.6-3.8",
            "cuDNN": "8.0",
            "CUDA": "11.0",
        },
        {
            "tf_version": "tensorflow-2.3.0",
            "python": "3.5-3.8",
            "cuDNN": "7.6",
            "CUDA": "10.1",
        },
        {
            "tf_version": "tensorflow-2.2.0",
            "python": "3.5-3.8",
            "cuDNN": "7.6",
            "CUDA": "10.1",
        },
    ]
    return json_data


def pytorch_compat_matrix():
    json_data = [
        {
            "torch_version": "2.3",
            "python": ">=3.8, <=3.11",
            "CUDA": "11.8",
            "cuDNN": "8.7",
        },
        {
            "torch_version": "2.2",
            "python": ">=3.8, <=3.11",
            "CUDA": "11.8",
            "cuDNN": "8.7",
        },
        {
            "torch_version": "2.1",
            "python": ">=3.8, <=3.11",
            "CUDA": "11.8",
            "cuDNN": "8.7",
        },
        {
            "torch_version": "2.0",
            "python": ">=3.8, <=3.11",
            "CUDA": "11.7",
            "cuDNN": "8.5",
        },
        {
            "torch_version": "1.13",
            "python": ">=3.7, <=3.10",
            "CUDA": "11.6",
            "cuDNN": "8.5",
        },
        {
            "torch_version": "1.12",
            "python": ">=3.7, <=3.10",
            "CUDA": "11.3",
            "cuDNN": "8.3",
        },
    ]

    return json_data


# this GPU only!
def find_correct_image_by_tf_gpu_only(tf_version):
    image_list = get_image_tag_from_docker()
    tf_matrix_list = tf_compat_matrix()
    for item in tf_matrix_list:
        if tf_version in item["tf_version"]:
            tf_cu_dnn_version = item["cuDNN"].split(".")[0]
            tf_cuda = item["CUDA"]
            for image_tag in image_list:
                splited_tag_name = image_tag.split("-")
                if (
                    tf_cuda in splited_tag_name[0]
                    and tf_cu_dnn_version in splited_tag_name[1]
                ):
                    return "nvidia/cuda:{}".format(image_tag)
    raise Exception(
        "RockAI can't find a suppported CUDA or cuDNN version for tensorflow version: {}".format(
            tf_version
        )
    )


def find_correct_image_by_torch_gpu_only(torch_version):
    image_list = get_image_tag_from_docker()
    torch_compat_list = pytorch_compat_matrix()
    for item in torch_compat_list:
        if item["torch_version"] in torch_version:
            cuda_version = item["CUDA"]
            cudnn_version = item["cuDNN"].split(".")[0]
            for image_tag in image_list:
                splited_tag_name = image_tag.split("-")
                if (
                    cuda_version in splited_tag_name[0]
                    and cudnn_version in splited_tag_name[1]
                ):
                    return "nvidia/cuda:{}".format(image_tag)

    raise Exception(
        "Rock can't find a suppported Cuda or cuDNN version for torch version: {}".format(
            torch_version
        )
    )


def parse_data(result):
    r_list = result["results"]
    result = []
    for item in r_list:
        if (
            "ubuntu" in item["name"]
            and "devel" in item["name"]
            and "cudnn" in item["name"]
        ):
            result.append(item["name"])
    return result


def get_image_tag_from_docker():

    result = []
    page = 1
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(
            description="Downloading image list...(should take around 10-15 seconds)",
            total=None,
        )
        while True:
            url = "https://hub.docker.com/v2/namespaces/nvidia/repositories/cuda/tags?page={}&page_size=100".format(
                page
            )
            response = requests.request("GET", url)

            if response.status_code == 200:
                result += parse_data(response.json())
            elif response.status_code == 404:
                break
            else:
                raise Exception()
            page += 1
        with open("nvidia_docker_cuda_image.json", "w") as file:
            json.dump(result, file)
        return result


def process_requirements(filename):
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            line_spl = line.split("==")
            if "tensorflow" == line_spl[0]:
                return "tensorflow", line_spl[1]
            if "torch" == line_spl[0]:
                return "torch", line_spl[1]


def build_final_image(config_map, port=8000):
    if config_map["build"]["gpu"] is True:
        # Build GPU image
        framework, version = process_requirements(
            Path.cwd() / config_map["build"]["python_requirements"]
        )
        if framework == "tensorflow":
            # image_tag = find_correct_image_by_tf_gpu_only(version)
            image_tag = 'nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04'
            print("building an tensorflow image")
            build_docker_image(image_tag, config_map, config_map["image"], port=port)
        elif framework == "torch":
            print("building an torch image")
            image_tag = find_correct_image_by_torch_gpu_only(version)
            build_docker_image(image_tag, config_map, config_map["image"], port=port)
        else:
            raise Exception(
                "No TensorFlow or PyTorch found in {} file".format(
                    Path.cwd() / config_map["build"]["python_requirements"]
                )
            )
    else:
        # build CPU image
        py_version = config_map["build"]["python_version"]
        build_cpu_image("python:{}".format(py_version), config_map, config_map["image"], port=port)


                    

def add_base(base):
    return "FROM {}\n".format(base)


def add_cmd(cmd_list):
    return "CMD {}\n".format(cmd_list)


def add_expose(port):
    return "EXPOSE {}\n".format(port)


def add_work_dir(dir):
    return "WORKDIR {}\n".format(dir)


def add_run(cmd):
    return "RUN {}\n".format(cmd)


def copy_files(src, dest):
    return "COPY {} {}\n".format(src, dest)


def add_env(env):
    return "ENV {}\n".format(env)


def save_docker_file(cmd_list):
    result = "".join(cmd_list)
    # Define the directory path
    directory_path = Path(str(Path.cwd() / 'temp'))

    # Check if the directory exists
    if not directory_path.exists():
        # If it does not exist, create the directory
        directory_path.mkdir(parents=True, exist_ok=True)
        print(f"Directory created: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")
    try:
        suffix = uuid.uuid4().hex
        with open(Path.cwd() / "temp/Dockerfile".format(suffix), "w") as file:
            file.write(result)
    except Exception as e:
        print("An error occurred while writing to the file. Error: ", str(e))

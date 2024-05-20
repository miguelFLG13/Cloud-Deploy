#! /usr/bin/python
import json
import os
import sys
from pypendency.builder import container_builder
from pypendency.loaders.yaml_loader import YamlLoader
from zipfile import ZipFile

from environments import PREPRODUCTION_ENVIRONMENT, PRODUCTION_ENVIRONMENT


if len(sys.argv) != 2:
    print("Incorrect Number of Parameters Error")
    sys.exit(1)

environments = [PRODUCTION_ENVIRONMENT, PREPRODUCTION_ENVIRONMENT]
if not sys.argv[1] in environments:
    print("Environment Argument Error")
    sys.exit(1)

environment = sys.argv[1]

YamlLoader(container_builder).load_dir(
    "{}/use_cases/_dependencies/".format(os.getcwd())
)

use_case = container_builder.get(
    "use_cases.deploy_serverless_code_use_case.DeployServerlessCodeUseCase"
)

use_case_image = container_builder.get(
    "use_cases.deploy_serverless_image_use_case.DeployServerlessImageUseCase"
)


with open("../serverless.{}.json".format(environment.lower())) as file:
    serverless_data = json.loads(file.read())

current_directory = os.getcwd()
for serverless_info in serverless_data:
    if serverless_info.get("image_repository"):
        use_case_image.deploy(environment, serverless_info)
    else:
        use_case.deploy(environment, serverless_info)

    os.chdir(current_directory)


use_case = container_builder.get(
    "use_cases.config_serverless_code_use_case.ConfigServerlessCodeUseCase"
)

with open("../serverless.{}.json".format(environment.lower())) as file:
    serverless_data = json.loads(file.read())

current_directory = os.getcwd()
for serverless_info in serverless_data:
    use_case.deploy(environment, serverless_info)
    os.chdir(current_directory)

print("LAMBDAS DEPLOYED")

use_case = container_builder.get(
    "use_cases.config_serverless_code_use_case.ConfigServerlessCodeUseCase"
)

with open("../serverless.{}.json".format(environment.lower())) as file:
    serverless_data = json.loads(file.read())

current_directory = os.getcwd()
for serverless_info in serverless_data:
    use_case.configure(environment, serverless_info)
    os.chdir(current_directory)

print("LAMBDAS CONFIGURED")

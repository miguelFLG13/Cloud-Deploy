#! /usr/bin/python
import json
import os
import sys
from pypendency.builder import container_builder
from pypendency.loaders.yaml_loader import YamlLoader

from environments import PREPRODUCTION_ENVIRONMENT, PRODUCTION_ENVIRONMENT


if len(sys.argv) != 3:
    print("Incorrect Number of Parameters Error")
    sys.exit(1)

environments = [PRODUCTION_ENVIRONMENT, PREPRODUCTION_ENVIRONMENT]
if not sys.argv[1] in environments:
    print("Environment Argument Error")
    sys.exit(1)

environment = sys.argv[1]
layer_zip_file_name = sys.argv[2]

YamlLoader(container_builder).load_dir(
    "{}/use_cases/_dependencies/".format(os.getcwd())
)

use_case = container_builder.get(
    "use_cases.create_serverless_layer_version_use_case.CreateServerlessLayerVersionUseCase"
)

with open("../serverless.{}.json".format(environment.lower())) as file:
    serverless_data = json.loads(file.read())

use_case.create(environment, serverless_data[0], "../{}".format(layer_zip_file_name))

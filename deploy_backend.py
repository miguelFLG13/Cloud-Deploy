#! /usr/bin/python
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

if not os.path.exists(sys.argv[2]):
    print("Path Argument Error")
    sys.exit(1)

environment = sys.argv[1]
path = sys.argv[2]

YamlLoader(container_builder).load_dir('{}/use_cases/_dependencies/'.format(os.getcwd()))

use_case = container_builder.get(
    "use_cases.deploy_serverless_code_use_case.DeployServerlessCodeUseCase"
)

use_case.deploy(environment, path)

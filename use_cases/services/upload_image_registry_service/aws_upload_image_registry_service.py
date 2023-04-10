import os

from use_cases.services.upload_image_registry_service.upload_image_registry_service import UploadImageRegistryService


class AwsUploadImageRegistryService(UploadImageRegistryService):
    """ Service to upload a docker image in ECR """

    def upload(self, image: DockerImage) -> None:
        account_id = os.getenv('ACCOUNT_ID')
        region = os.getenv('REGION_NAME')
        os.system("docker build . -t {image.tag}")
        docker_login_command = os.popen("aws ecr get-login --region eu-west-2").read()
        docker_login_command = docker_login_command.replace("-e none", "")
        os.system(docker_login_command)
        os.system(f"docker tag {image.tag}:latest {account_id}.dkr.ecr.{region}.amazonaws.com/{image.repository}:latest")
        os.system(f"docker push {account_id}.dkr.ecr.{region}.amazonaws.com/{image.repository}:latest")
from globus_compute_sdk import Client, Executor
from .custom_image_builder import build_and_register_container
from .custom_image_builder.image_builder import redef_in_main
import traceback
import os
import requests
import json
from typing import Union

class ImageRegistry:
    """
    This class provides methods for building images, checking if an image exists in the registry, and listing containers.
    """

    IMAGES_FOLDER = ".images"
    REGISTRY_FILE_NAME = "registry.json"
    BASE_IMAGE_CATALOG_URL = "https://catalog.ngc.nvidia.com/api/containers/images?orgName=nvidia&name=pytorch&isPublic=true"
    BASE_IMAGE_PREFIX = "nvcr.io/nvidia/pytorch:"

    def __init__(self, site_config: dict):
        """
        Initialize the ImageRegistry with a specific site configuration.

        :param site_config: The config for an endpoint
        """
        self.site_config = site_config
        self.gcc_client = Client()
        self.endpoint = site_config['endpoint']
        self.images_dir = os.path.join(site_config['work_path'], self.IMAGES_FOLDER)
        self.registry_file_path = os.path.join(self.images_dir, self.REGISTRY_FILE_NAME)
        print("Loading the image registry...")
        # the registry is a dictionary with image file names as keys and container ids as values
        import __main__
        with Executor(endpoint_id=self.endpoint) as ex:
            redef_in_main(funcx_get_registry)
            fut = ex.submit(__main__.funcx_get_registry, self.registry_file_path)
        self.registry = fut.result()

    def build(self, base_img: str, pkg_config: Union[str, list], img_file_name: str, base_img_type: str = "docker", force: bool = False) -> str:
        """
        This function lets users build an apptainer image with a base image and a required package config on an endpoint.

        :param base_img: The name of the base image
        :param pkg_config: Pip package configuration, a file path or a list of packages
        :param img_file_name: The name of the image file
        :param base_img_type: The type of the base image
        :param force: If True, the image will be built even if it already exists
        :return: The built container id
        """
        if not force and self.exists(img_file_name):
            print(f"The image [{img_file_name}] already exists in the registry.")
            return self.registry[img_file_name]
        
        pip_packages = []
        if isinstance(pkg_config, list):
            pip_packages = pkg_config
        elif isinstance(pkg_config, str):
            if not os.path.exists(pkg_config):
                print("The package config file does not exist.")
            else:
                with open(pkg_config, 'r') as f:
                    pip_packages = f.read().strip().split("\n")
        print(f"The pip packages to be installed are {pip_packages}")

        try:
            container_id = build_and_register_container(gcc_client=self.gcc_client,
                                                        endpoint_id=self.endpoint,
                                                        image_file_name=img_file_name,
                                                        base_image_type=base_img_type,
                                                        base_image=base_img,
                                                        images_dir=self.images_dir,
                                                        pip_packages=pip_packages
                                                        )
            # update the image registry
            self.update_registry(img_file_name, container_id)
            return container_id
        except Exception as e:
            traceback.print_exc()
            return None

    def exists(self, img_file_name: str) -> bool:
        """
        This function checks if an image is already in the local registry.

        :param img_file_name: The name of the image file
        :return: True if the image is in the registry, otherwise False
        """
        return img_file_name in self.registry
    
    def update_registry(self, img_file_name: str, container_id: str):
        """
        This function updates the local registry with a new image.

        :param img_file_name: The name of the image file
        :param container_id: The container id
        """
        self.registry[img_file_name] = container_id
        import __main__
        with Executor(endpoint_id=self.endpoint) as ex:
            redef_in_main(funcx_update_registry)
            fut = ex.submit(__main__.funcx_update_registry, self.registry_file_path, self.registry)
        # wait for the update to finish
        fut.result()

    def list_avail_containers(self):
        """
        This function lists all the available Apptainer containers on an endpoint.
        """
        return self.registry

    def list_base_image_tags(self):
        """
        This function lists all the available base image tags from a third-party registry.
        """
        images_info = json.loads(requests.get(self.BASE_IMAGE_CATALOG_URL).text)['images']
        tags = [x['tag'] for x in images_info]
        full_tags = [f"{self.BASE_IMAGE_PREFIX}{x}" for x in tags]
        return full_tags
    

def funcx_get_registry(registry_file_path):
    """
    This function is supposed to be submitted by the client and returns the registry dictionary.

    :param registry_file_path: The path to the registry file on the endpoint
    :return: The registry dictionary
    """
    import json
    import os

    registry = {}
    if os.path.exists(registry_file_path):
        # load the registry json file
        with open(registry_file_path, 'r') as f:
            registry = json.load(f)
    return registry


def funcx_update_registry(registry_file_path, registry):
    """
    This function is supposed to be submitted by the client and updates the registry file on the endpoint.

    :param registry_file_path: The path to the registry file on the endpoint
    :param registry: The registry dictionary
    """
    import json

    with open(registry_file_path, 'w') as f:
        json.dump(registry, f)


if __name__ == "__main__":
    site_config = {
        "endpoint": "847f59fb-7286-452c-b490-0270ddd8da94",
        "work_path": "/work2/09849/gcyang/frontera"
    }
    ir = ImageRegistry(site_config)

    print("The available base image tags are:")
    print(ir.list_base_image_tags())

    print("The available containers are:")
    print(ir.list_avail_containers())

    # pick a base image from https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch/tags
    base_img = "nvcr.io/nvidia/pytorch:24.02-py3"
    # save an example of pip config to a file
    example_pkg_str = "lightning\nscipy\n"
    pkg_config_path = "/tmp/pip_config.txt"
    with open(pkg_config_path, 'w') as f:
        f.write(example_pkg_str)
    img_file_name = "nv_pytorch"
    container_id = ir.build(base_img, pkg_config_path, img_file_name)
    if container_id:
        print(f"The container id is {container_id}")
    else:
        print("Failed to build the container.")

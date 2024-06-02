import os
import pkg_resources
import platform
import tempfile

from diamond.container.container import ImageRegistry
from globus_sdk import NativeAppAuthClient
from globus_compute_sdk.sdk.login_manager.globus_auth  import internal_auth_client
from globus_compute_sdk.sdk.login_manager.manager import LoginManager


class DiamondClient:

    def __init__(self):
        pass

    def get_auth_client(self):
        auth_client = internal_auth_client()
        login_manager = LoginManager()
        scopes = [
            s for _rs_name, rs_scopes in login_manager.login_requirements for s in rs_scopes
        ]
        auth_client.oauth2_start_flow(
            redirect_uri=auth_client.base_url + "v2/web/auth-code",
            refresh_tokens=True,
            requested_scopes=scopes,
            prefill_named_grant=platform.node(),
        )
        return auth_client

    def get_oauth2_url(self, auth_client: NativeAppAuthClient):
        query_params = {"prompt": "login"}
        oauth2_url = auth_client.oauth2_get_authorize_url(query_params=query_params)
        return oauth2_url
    
    def oauth2_login_by_token(self, auth_client: NativeAppAuthClient, auth_code: str):
        return auth_client.oauth2_exchange_code_for_tokens(auth_code)

    def write_auth_token_to_db(self, oauth_token_response: str):
        login_manager = LoginManager()
        with login_manager._access_lock:
            login_manager._token_storage.store(oauth_token_response)

    def generate_temp_file(self):
        return tempfile.mktemp()

    def generate_task_script(self, cmd: str, log_path: str, endpoint_id: str, container_id: str):
        task_template_filepath = pkg_resources.resource_filename(
            'diamond','diamond_client/templates/task_template')
        tmp_script_path = self.generate_temp_file()
        with open(task_template_filepath, 'r') as f:
            task_template = f.read()
            task_script = (
                task_template
                .replace("dummy_command", cmd)
                .replace("dummy_log_path", log_path)
                .replace("dummmy_endpoint_id", endpoint_id)
                .replace("dummy_container_id", container_id)
            )
            with open(tmp_script_path, 'w') as f:
                f.write(task_script)
        print(tmp_script_path)
        return tmp_script_path
    
    def run_task(self, cmd: str, log_path: str, endpoint_id: str, container_id: str):
        task_script_path = self.generate_task_script(cmd, log_path, endpoint_id, container_id)
        return os.system(f'python3 {task_script_path}')
    
    def register_container(
            self,
            endpoint_id: str,
            work_path: str,
            image_file_name: str,
            base_image: str):
        site_config = {
            "endpoint": endpoint_id,
            "work_path": work_path,
        }
        ir = ImageRegistry(site_config)
        container_id = ir.build(base_image, None, image_file_name)
        return container_id

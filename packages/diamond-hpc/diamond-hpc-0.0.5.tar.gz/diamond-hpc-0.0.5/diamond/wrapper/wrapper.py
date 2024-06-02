import click

from diamond.diamond_client.diamond_client import DiamondClient


def execute_task(cmd: str, log_path: str, endpoint_id: str, container_id: str):
    diamond = DiamondClient()
    return diamond.run_task(cmd, log_path, endpoint_id, container_id)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--cmd', required=True, help='Command to run task')
@click.option('--log_path', required=True, help='Log file path in the supercomputer')
@click.option('--endpoint_id', required=True, help='Endpoint ID')
@click.option('--container_id', required=True, help='Container ID')
def run_task(cmd: str, log_path: str, endpoint_id: str, container_id: str):
    click.echo(execute_task(cmd, log_path, endpoint_id, container_id))


@cli.command()
@click.option('--cmd_script', required=True, help='Task command script file path')
@click.option('--log_path', required=True, help='Log file path in the supercomputer')
@click.option('--endpoint_id', required=True, help='Endpoint ID')
@click.option('--container_id', required=True, help='Container ID')
def run_task_from_script(cmd_script: str, log_path: str, endpoint_id: str, container_id: str):
    with open(cmd_script, 'r') as f:
        cmd = f.read()
    click.echo(execute_task(cmd, log_path, endpoint_id, container_id))


@cli.command()
@click.option('--endpoint_id', required=True, help='Endpoint ID')
@click.option('--work_path', required=True, help='Work path')
@click.option('--image_file_name', required=True, help='Image file name')
@click.option('--base_image', required=True, help='Base image name in docker hub')
def register_container(endpoint_id: str,work_path: str,image_file_name: str,base_image: str):
    diamond = DiamondClient()
    container_id = diamond.register_container(endpoint_id, work_path, image_file_name, base_image)
    click.echo(f"The container id is {container_id}")


@cli.command()
def get_oauth2_url_and_login():
    diamond = DiamondClient()
    auth_client = diamond.get_auth_client()
    click.echo(diamond.get_oauth2_url(auth_client))
    auth_code = input()
    oauth_token_response = diamond.oauth2_login_by_token(auth_client, auth_code)
    diamond.write_auth_token_to_db(oauth_token_response)
    click.echo("Login successfully")


if __name__ == '__main__':
    cli()

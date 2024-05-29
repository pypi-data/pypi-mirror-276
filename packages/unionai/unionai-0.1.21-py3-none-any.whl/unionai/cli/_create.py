import re
import time
from pathlib import Path
from typing import Optional

import rich_click as click
from flytekit import WorkflowExecutionPhase
from flytekit.configuration import AuthType, ImageConfig, PlatformConfig, SerializationSettings
from flytekit.models.core.execution import TaskExecutionPhase
from grpc import RpcError
from rich.console import Console

from unionai._config import (
    _UNIONAI_CONFIG,
    AppClientCredentials,
    _encode_app_client_credentials,
    _get_config_obj,
    _get_user_handle,
    _is_serverless_endpoint,
    _write_config_to_path,
)
from unionai.cli._common import _get_channel_with_org
from unionai.internal.identity.app_payload_pb2 import CreateAppRequest
from unionai.internal.identity.app_service_pb2_grpc import AppsServiceStub
from unionai.internal.identity.enums_pb2 import (
    ConsentMethod,
    GrantTypes,
    ResponseTypes,
    TokenEndpointAuthMethod,
)
from unionai.internal.secret.definition_pb2 import SecretIdentifier, SecretSpec
from unionai.internal.secret.payload_pb2 import CreateSecretRequest
from unionai.internal.secret.secret_pb2_grpc import SecretServiceStub
from unionai.remote import UnionRemote
from unionai.workspace._vscode import (
    _DEFAULT_CONFIG_YAML_FOR_BASE_IMAGE,
    _DEFAULT_CONFIG_YAML_FOR_IMAGE_SPEC,
    WorkspaceConfig,
    resolver,
)
from unionai.workspace._vscode_remote import _generate_workspace_name, _get_workspace_executions


@click.group()
def create():
    """Create a resource."""


@create.command()
@click.pass_context
@click.argument("name")
@click.option("--value", prompt="Enter secret value", help="Secret value", hide_input=True)
@click.option("--project", help="Project name")
@click.option("--domain", help="Domain name")
def secret(
    ctx: click.Context,
    name: str,
    value: str,
    project: Optional[str],
    domain: Optional[str],
):
    """Create a secret with NAME."""
    platform_obj = _get_config_obj(ctx.obj.get("config_file", None)).platform
    channel, org = _get_channel_with_org(platform_obj)

    stub = SecretServiceStub(channel)
    request = CreateSecretRequest(
        id=SecretIdentifier(name=name, domain=domain, project=project, organization=org),
        secret_spec=SecretSpec(value=value),
    )
    try:
        stub.CreateSecret(request)
        click.echo(f"Created secret with name: {name}")
    except RpcError as e:
        raise click.ClickException(f"Unable to create secret with name: {name}\n{e}") from e


@create.command()
@click.pass_context
@click.argument("client_name")
def app(
    ctx: click.Context,
    client_name: str,
):
    """Create a app with CLIENT_NAME."""
    platform_obj = _get_config_obj(ctx.obj.get("config_file", None)).platform
    normalized_client_name = re.sub("[^0-9a-zA-Z]+", "-", client_name.lower())
    if _is_serverless_endpoint(platform_obj.endpoint):
        userhandle = _get_user_handle(platform_obj)
        tenant = _UNIONAI_CONFIG.serverless_endpoint.split(".")[0]
        client_id = f"{tenant}-{userhandle}-{normalized_client_name}"
    else:
        client_id = normalized_client_name
    channel, org = _get_channel_with_org(platform_obj)

    stub = AppsServiceStub(channel)
    request = CreateAppRequest(
        organization=org,
        client_id=client_id,
        client_name=client_id,
        grant_types=[GrantTypes.CLIENT_CREDENTIALS, GrantTypes.AUTHORIZATION_CODE],
        redirect_uris=["http://localhost:8080/authorization-code/callback"],
        response_types=[ResponseTypes.CODE],
        token_endpoint_auth_method=TokenEndpointAuthMethod.CLIENT_SECRET_BASIC,
        consent_method=ConsentMethod.CONSENT_METHOD_REQUIRED,
    )

    try:
        response = stub.Create(request)
    except RpcError as e:
        raise click.ClickException(f"Unable to create app with name: {client_name}\n{e}") from e

    click.echo(f"Client ID: {response.app.client_id}")
    click.echo("The following API key will only be shown once. Be sure to keep it safe!")
    click.echo("Configure your headless CLI by setting the following environment variable:")
    click.echo()

    serverless_api_key = _encode_app_client_credentials(
        AppClientCredentials(
            endpoint=platform_obj.endpoint,
            client_id=response.app.client_id,
            client_secret=response.app.client_secret,
            org=org,
        )
    )
    click.echo(f'export UNIONAI_SERVERLESS_API_KEY="{serverless_api_key}"')


@create.command()
@click.pass_context
@click.argument("auth", type=click.Choice(["device-flow", "pkce"]))
def login(ctx: click.Context, auth: str):
    """Create login."""
    config_obj = _get_config_obj(ctx.obj.get("config_file", None))

    if auth == "pkce":
        auth_mode = AuthType.PKCE
    else:
        auth_mode = AuthType.DEVICEFLOW

    config = config_obj.with_params(
        platform=PlatformConfig(
            endpoint=config_obj.platform.endpoint,
            insecure=False,
            auth_mode=auth_mode,
        )
    )
    remote = UnionRemote(config=config)

    try:
        # Accessing the client will trigger authentication
        remote.client
        _write_config_to_path(config.platform.endpoint, auth_mode.value)
        click.echo(f"Login successful! `unionai` CLI will now use '{auth}' for authentication.")

    except Exception as e:
        raise click.ClickException(f"Unable to login.\n{e}") from e


@create.command()
@click.pass_context
@click.argument("config_file", type=click.Path(path_type=Path))
def workspace(ctx: click.Context, config_file: Path):
    """Create workspace."""
    config_content = config_file.read_text()
    workspace_config = WorkspaceConfig.from_yaml(config_content)

    config_obj = _get_config_obj(ctx.obj.get("config_file", None))
    remote = UnionRemote(
        config=config_obj, default_domain=workspace_config.domain, default_project=workspace_config.project
    )
    _create_workspace(remote, workspace_config, config_content)


@create.command("workspace-config")
@click.argument("config_file", type=click.Path(path_type=Path))
@click.option("--init", type=click.Choice(["base_image", "image_spec"]), required=True)
def workspace_config(config_file: Path, init: str):
    """Create workspace config at CONFIG_FILE."""
    if config_file.exists():
        raise click.ClickException(f"{config_file} already exists")

    click.echo(f"Writing workspace configuration to {config_file}")
    if init == "base_image":
        config_file.write_text(_DEFAULT_CONFIG_YAML_FOR_BASE_IMAGE)
    else:
        config_file.write_text(_DEFAULT_CONFIG_YAML_FOR_IMAGE_SPEC)


def _create_workspace(remote: UnionRemote, ws_config: WorkspaceConfig, config_content: str):
    name = ws_config.name
    project = ws_config.project
    domain = ws_config.domain

    executions = _get_workspace_executions(remote, project, domain)

    for execution, ex_name in executions:
        if ex_name == name:
            raise click.ClickException(f"Workspace with name: {name} already exists.")

    task = resolver.get_task_for_workspace(ws_config)
    console = Console()
    console.print("✨ Creating workspace...")

    try:
        source_root = task.container_image.source_root
    except AttributeError:
        source_root = None

    remote_task = remote.register_task(
        task,
        serialization_settings=SerializationSettings(
            project=project, domain=domain, image_config=ImageConfig.auto_default_image(), source_root=source_root
        ),
        version=_generate_workspace_name(name),
    )

    execution = remote.execute(
        remote_task,
        inputs={"config_content": config_content},
        project=project,
        domain=domain,
    )

    vscode_count = 0
    with console.status("✨ Starting workspace...") as status:
        status.update(status="🚀 Starting workspace...")
        while True:
            time.sleep(5)
            execution = remote.sync_execution(execution, sync_nodes=True)
            if execution.is_done:
                url = remote.generate_console_url(execution)
                raise click.ClickException(f"Workspace failed to launch. See {url} for details.")

            if execution.closure.phase != WorkflowExecutionPhase.RUNNING:
                continue

            status.update(status="⏳ Waiting for node to spin up...")
            if not execution.node_executions:
                continue

            all_keys = [e for e in execution.node_executions if e != "start-node"]
            if not all_keys:
                continue

            vscode_key = all_keys[0]
            vscode_node = execution.node_executions[vscode_key]

            if vscode_node.closure.phase != TaskExecutionPhase.RUNNING or not vscode_node.task_executions:
                continue

            task_execution = vscode_node.task_executions[-1]
            if task_execution.closure.phase != TaskExecutionPhase.RUNNING:
                continue

            for log in task_execution.closure.logs:
                if "VSCode" in log.name:
                    status.update(status="⏳ Waiting for VSCode to start...")
                    resolve_uri = remote.generate_console_http_domain() + log.uri
                    vscode_count += 1
                    if vscode_count == 3:
                        # Make sure execution did not fail before showing dynamic log link
                        execution = remote.sync_execution(execution, sync_nodes=True)
                        if execution.is_done:
                            url = remote.generate_console_url(execution)
                            raise click.ClickException(f"Workspace failed to launch. See {url} for details.")

                        click.echo(f"\n🚀 Open Workspace at:\n{resolve_uri}")
                        return

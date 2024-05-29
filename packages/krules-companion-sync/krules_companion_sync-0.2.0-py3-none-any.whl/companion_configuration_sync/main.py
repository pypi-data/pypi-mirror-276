import sys
from datetime import datetime
import re

import typer
import yaml
import firebase_admin
from firebase_admin import firestore
from rich.console import Console
from rich import print
from typing import Optional
from typing_extensions import Annotated

app = typer.Typer()

err_console = Console(stderr=True)


def read_yaml_file(yaml_file: str) -> dict:
    """Read YAML file and return its content."""
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)


def create_or_update_doc(db, collection_path, document_id, data):
    """Check if document exists. If not create a new one if instead exists update document data"""
    doc_ref = db.collection(collection_path).document(document_id)
    if doc_ref.get().exists:
        firestore_data = doc_ref.get().to_dict()
        if firestore_data != data:
            doc_ref.set(data)
            print(f"'{document_id}' in Firestore updated.")
        else:
            print(f"'{document_id}' in Firestore is already up to date.")
    else:
        doc_ref.set(data)
        print(f"'{document_id}' created in Firestore.")


def update_channels(db, yaml_data: dict):
    """Update channels."""
    subscription_id = yaml_data.get('subscription')
    channels_data = yaml_data.get('channels', {})
    collection_path = f"{subscription_id}/settings/channels"
    print("Checking Channels...")
    for channel_id, channel_data in channels_data.items():
        channel_data["slug"] = re.sub(r'[\W_]+', '-', channel_id)
        create_or_update_doc(db, collection_path, channel_id, channel_data)


def update_triggers(db, yaml_data: dict):
    """Update triggers."""
    subscription_id = yaml_data.get('subscription')
    triggers_data = yaml_data.get('triggers', {})
    collection_path = f"{subscription_id}/settings/automations"
    for position, obj in enumerate(triggers_data.items()):
        automation_id, trigger_data = obj
        trigger_data["createdAt"] = datetime.utcnow()
        trigger_data["position"] = position
        trigger_data["createdBy"] = "cm-sync"
        trigger_data["running"] = True
        trigger_data["id"] = automation_id
        print("Checking Triggers...")
        trigger_channels = trigger_data.get('channels', [])
        channels_data = set(get_channel_names_from_firestore(db, f"{subscription_id}/settings/channels"))
        for channel in trigger_channels:
            if channel not in channels_data:
                err_console.print(
                    f"Error: Channel '{channel}' specified under trigger '{automation_id}' does not exist.")
                break
        else:
            create_or_update_doc(db, collection_path, automation_id, trigger_data)


def get_channel_names_from_firestore(db, collection_path):
    channel_names = []
    channels_ref = db.collection(collection_path)
    channels = channels_ref.stream()
    for channel in channels:
        channel_names.append(channel.id)
    return channel_names


@app.command()
def sync(
        yaml_file: str = typer.Argument(
            None, help="Il nome del file yaml da processare. Se non fornito, legge da stdin."
        ),
        subscription: Annotated[Optional[int], typer.Option(envvar="COMPANION_SUBSCRIPTION",
                                                            help="Subscription id (override defaults)")] = None,
        credentials: Annotated[Optional[str], typer.Option(envvar="GOOGLE_APPLICATION_CREDENTIALS",
                                                           help="Google credentials")] = None,
        project_id: Annotated[Optional[str], typer.Option(envvar="COMPANION_PROJECT_ID",
                                                          help="Project id")] = None,
):
    # Initialize the SDK with a service account
    cred = None
    if credentials is not None:
        cred = firebase_admin.credentials.Certificate(credentials)

    firebase_options = {}
    if project_id is not None:
        firebase_options["projectId"] = project_id
    firebase_admin.initialize_app(credential=cred, options=firebase_options)
    db = firestore.client()
    """Update channels."""
    if yaml_file is None:
        try:
            yaml_data = sys.stdin.read()  # Read from standard input (pipe)
            yaml_data = yaml.safe_load(yaml_data)
        except FileNotFoundError:
            err_console.print(f"Error: The file {yaml_file} is not in the correct format.")
            raise typer.Exit(code=1)

    else:
        yaml_data = read_yaml_file(yaml_file)  # Use yaml_file directly
    if subscription is not None:
        yaml_data["subscription"] = subscription
    if yaml_data.get("subscription") is None:
        err_console.print(f"Error: 'subscription' is not defined.")
        raise typer.Exit(code=1)
    update_channels(db, yaml_data)
    update_triggers(db, yaml_data)


def entry_point():
    typer.run(sync)


if __name__ == "__main__":
    app()

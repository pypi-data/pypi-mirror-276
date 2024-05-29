import argparse

import requests

from ambientctl.config import settings


def get_parser():
    parser = argparse.ArgumentParser(
        prog="daemon",
        usage="ambientctl %(prog)s [options] [action]",
        description="Manage the Ambient Edge Server daemon.",
        epilog="Example: ambientctl %(prog)s restart",
        add_help=False,  # Suppress the default help argument
    )
    parser.add_argument("action", help="The action to perform on the service.")
    return parser


def run(args):
    action = args.action
    if action == "install":
        print("Installing service ...")
        print("NOTE: You will be asked for your password.")
        install()
    elif action == "start":
        print("Starting service ...")
        start()
    elif action == "stop":
        print("Stopping service ...")
        stop()
    elif action == "restart":
        print("Restarting service ...")
        restart()

    elif action == "status":
        print("Getting service status ...")
        status()
    else:
        print("Invalid action.")
        exit(1)


def install():
    try:
        url = f"{settings.ambient_server}/daemon/install"
        response = requests.post(url)
        response.raise_for_status()
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Failed to install service: {e}")
        exit(1)


def start():
    try:
        url = f"{settings.ambient_server}/daemon/start"
        response = requests.post(url)
        response.raise_for_status()
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Failed to start service: {e}")
        exit(1)


def stop():
    try:
        url = f"{settings.ambient_server}/daemon/stop"
        response = requests.post(url)
        response.raise_for_status()
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Failed to stop service: {e}")
        exit(1)


def restart():
    try:
        url = f"{settings.ambient_server}/daemon/restart"
        response = requests.post(url)
        response.raise_for_status()
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Failed to restart service: {e}")
        exit(1)


def status():
    try:
        url = f"{settings.ambient_server}/daemon/status"
        response = requests.get(url)
        response.raise_for_status()
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Failed to get service status: {e}")
        exit(1)

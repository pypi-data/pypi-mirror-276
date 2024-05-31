from pathlib import Path

import requests

REQUEST_TIMEOUT = 120


def get_trajectory_ptr(crema_id, output_folder):
    """Downloads the PTR associated to the trajectory and stores it in the
    output folder

    Args:
        crema_id (str): _description_
        output_folder (str | path): target folder

    Returns:
        str: file path of the PTR associated to the trajectory
    """
    response = requests.get(
        f"https://juicesoc.esac.esa.int/rest_api/trajectory/{crema_id}/ptr",
        timeout=REQUEST_TIMEOUT)
    if response.status_code == requests.codes.ok:
        ptr_url = response.json().get("ptr_file")
        download = requests.get(ptr_url, timeout=REQUEST_TIMEOUT)
        if download.status_code == requests.codes.ok:
            ptr_path = Path(output_folder, f"{crema_id}.ptx")
            with ptr_path.open("wb") as file:
                file.write(download.content)
            return ptr_path
    return None

def get_trajectory_phases(crema_id):
    """Returns the trajectory phases

    Args:
        crema_id (str): _description_

    Returns:
        json object: list of phases
    """
    response = requests.get(f"https://juicesoc.esac.esa.int/rest_api/trajectory/{crema_id}/", timeout=REQUEST_TIMEOUT)
    trajectory = response.json()
    return trajectory.get("phases")


def __get_sht_config():
    response = requests.get("https://juicesoc.esac.esa.int/rest_api/config/", timeout=REQUEST_TIMEOUT)
    return response.json()

def get_targets():
    """Returns the target mnemonics available in SHT

    Returns:
        list of str: list of targets
    """
    config = __get_sht_config()
    return [item.get("mnemonic") for item in config.get("targets")]


def get_instrument_types():
    """Returns the instrument types mnemonics available in SHT

    Returns:
        list of str: list of instrument types
    """
    config = __get_sht_config()
    return [item.get("mnemonic") for item in config.get("instrument_types")]

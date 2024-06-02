from typing import Any, Dict, Final, List, Tuple
import washpy
import flask
import flask_caching
from washpy.device_user import DeviceUser
from washpy.state import State, Status
import threading
import argparse
import waitress

from dorfwash.config import DorfwashConfig

# ~~~ flask config ~~~
flask_config: Final[Dict[str, Any]] = {
    "DEBUG": False,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
}
app: Final[flask.Flask] = flask.Flask(__name__)
app.config.from_mapping(flask_config)
cache: Final[flask_caching.Cache] = flask_caching.Cache(app)

machines: Dict[str, washpy.DeviceUser] = {}


# caching is not thread-safe
@app.route("/")
@cache.cached(timeout=20)
def state():
    """
    generates an overview over all washing machines in HTML table format
    """
    table_data: List[Tuple[str, str]] = []

    def append_device_summary_to_table(device_name: str, device: DeviceUser) -> None:
        """
        device_name: name of the device

        device: device to query

        retrieves the device status, and appends a proper summary to `table_data`
        """
        print(f"processing device {device_name}")
        device_summary: str = ""
        try:
            state: State = device.get_state()

            if state.Status == Status.OFF:
                device_summary = "powered off"
            elif state.pRemainingTime is None:
                device_summary = "idle"
            else:
                remaining_seconds: int = int(state.pRemainingTime.total_seconds())
                hours: int = remaining_seconds // 3600
                remaining_seconds -= 3600 * hours
                minutes: int = remaining_seconds // 60
                remaining_seconds -= 60 * minutes
                device_summary = f"finishes in: {hours} hours, {minutes} minutes"
        except Exception as e:
            print(e)
            # table_data.append({device: "unknown"})
            # continue
            print("HELLO")
            device_summary = "unknown"

        table_data.append((device_name, device_summary))

    # get the device summary in parallel
    # the XKM web server is slow, requesting 5 machines sequentually takes >= 2 seconds,
    # i.e. is too slow for a responsive web app
    threads: List[threading.Thread] = [
        threading.Thread(
            target=append_device_summary_to_table, args=(device_name, device)
        )
        for device_name, device in machines.items()
    ]

    [t.start() for t in threads]
    [t.join() for t in threads]

    return flask.render_template("index.html", table_data=sorted(table_data))


def init_machines(config: DorfwashConfig) -> None:
    """
    fills the global machine table
    """
    for device in config.devices:
        print(f'initializing machine "{device.name}"')
        try:
            machines[device.name] = DeviceUser(
                device.url,
                device.username,
                device.password,
                verify_https=device.verify_https,
                https_timeout=config.https_timeout,
            )
        except Exception as e:
            print(f'skipping machine "{device.name}", an error has occoured: {e}')

    print("done initializing")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config", type=argparse.FileType("r"), help="path to the json config file"
    )
    args = parser.parse_args()
    config_json: str = args.config.read()
    print(config_json)
    config: DorfwashConfig = DorfwashConfig.model_validate_json(config_json)
    print(config)
    init_machines(config)
    waitress.serve(app, listen="*:8080")

import logging
from pathlib import Path

from steamcmd_wrapper.config import (
    GENERIC_ERRORS,
    IGNORED_ERRORS,
    ON_APP_UPDATE_SUCCESS_MSG,
    ON_LOGIN_MSG,
    ON_MOD_UPDATE_SUCCESS_MSG,
    ON_READY_MSG,
    SteamCMDDownloadTimeoutError,
)
from steamcmd_wrapper.steam_client.protocol_steamcmd_client import PSteamCMDClient
from steamcmd_wrapper.steam_downloader.file_system import PFileSystem
from steamcmd_wrapper.steam_subprocess.protocol_subprocess import PSubprocessProtocol


class SteamCMDClientInstallDirError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Can't install in same directory as steamcmd. SteamCMD will ignore new location",
        )


class SteamCMDClient(PSteamCMDClient):
    def __init__(self, subprocess: PSubprocessProtocol, file_system: PFileSystem) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.current_logged_user: str | None = None
        self.subprocess = subprocess
        self.file_system = file_system
        self.logger.info("Starting up subprocess")
        self.subprocess.start()
        self._wait_for_steam_cmd_output(ON_READY_MSG)
        self.logger.info("Started up subprocess")

    def login(
        self,
        username: str,
        password: str,
        token: str | None = None,
    ) -> None:
        self.logger.info("Logging in as username:")
        self.current_logged_user = username
        payload = f"login {username} {password}"
        if token:
            payload += f" {token}"
        self.subprocess.input(payload)
        self._wait_for_steam_cmd_output(ON_LOGIN_MSG)
        self.logger.info(f"Logged in as {username}")

    def login_as_anonymous(self) -> None:
        self.login("anonymous", "anonymous")

    def set_install_dir(self, install_dir: str) -> None:
        if self.file_system.is_file_in_directory(
            self.subprocess.executable_file,
            Path(install_dir),
        ):
            raise SteamCMDClientInstallDirError
        self.subprocess.input(f"force_install_dir {install_dir}")
        self.logger.info(f"Set install dir to {install_dir}")

    def update_app(self, app_id: str, validate: bool = True) -> None:
        self.logger.info(f"Updating app {app_id}")
        payload = f"app_update {app_id}"
        if validate:
            payload += " validate"
        self.subprocess.input(payload)
        self._wait_for_steam_cmd_output(ON_APP_UPDATE_SUCCESS_MSG)
        self.logger.info(f"Updated app {app_id}")

    def update_workshop_mod(self, app_id: str, mod_id: str, validate: bool = True) -> None:
        self.logger.info(f"Updating workshop mod {app_id}:{mod_id}")
        payload = f"workshop_download_item {app_id} {mod_id}"
        if validate:
            payload += " validate"
        self.subprocess.input(payload)
        try:
            self._wait_for_steam_cmd_output(ON_MOD_UPDATE_SUCCESS_MSG)
        except SteamCMDDownloadTimeoutError:
            self.logger.info("Retrying download after timeout...")
            self.update_workshop_mod(app_id, mod_id, validate)
        else:
            self.logger.info(f"Updated workshop mod {app_id}:{mod_id}")
            return

    def _wait_for_steam_cmd_output(self, success_msg: str) -> None:
        while True:
            output = self.subprocess.read_output()
            if success_msg in output:
                return
            self._check_output_for_errors(output)

    def _check_output_for_errors(self, output: str) -> None:
        for generic_error in GENERIC_ERRORS:
            if generic_error.error_msg.lower() in output.lower():
                if any(ignored_error.lower() in output.lower() for ignored_error in IGNORED_ERRORS):
                    return
                raise generic_error.exception(output)

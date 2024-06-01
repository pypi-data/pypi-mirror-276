import contextlib
import functools
import logging
import subprocess
import warnings
from typing import Optional
from warnings import warn

import esptool
from esptool import __version__ as ESPTOOL_VERSION
from esptool.targets import CHIP_LIST as ESPTOOL_CHIPS
from pexpect import TIMEOUT
from pytest_embedded.log import MessageQueue, PexpectProcess, live_print_call
from pytest_embedded.utils import Meta
from pytest_embedded_serial.dut import Serial


def _is_port_mac_verified(pexpect_proc: PexpectProcess, port: str, port_mac: str, msg_queue) -> bool:
    try:
        live_print_call(['esptool.py', '--port', port, 'read_mac'], msg_queue=msg_queue)
    except subprocess.CalledProcessError:
        return False
    else:
        try:
            pexpect_proc.expect(f'MAC: {port_mac.lower()}', timeout=0.1)
        except TIMEOUT:
            return False
        else:
            return True


class EsptoolArgs:
    """
    fake args object, this is a hack until esptool Python API is improved
    """

    def __init__(self, **kwargs):
        warnings.warn('EsptoolArgs is deprecated and will be removed in 2.0 release.', DeprecationWarning)

        for key, value in kwargs.items():
            self.__setattr__(key, value)


class EspSerial(Serial):
    """
    Serial class for ports connected to espressif products. Each object could be treated as one target chip.
    """

    ESPTOOL_DEFAULT_BAUDRATE = 921600

    def __init__(
        self,
        pexpect_proc: PexpectProcess,
        msg_queue: MessageQueue,
        target: Optional[str] = None,
        beta_target: Optional[str] = None,
        port: Optional[str] = None,
        port_mac: Optional[str] = None,
        baud: int = Serial.DEFAULT_BAUDRATE,
        esptool_baud: int = ESPTOOL_DEFAULT_BAUDRATE,
        flash_port: Optional[str] = None,  # more like a "reverse-dependency" for arduino and idf
        esp_flash_force: bool = False,  # more like a "reverse-dependency" for arduino and idf
        skip_autoflash: bool = False,  # more like a "reverse-dependency" for arduino and idf
        erase_all: bool = False,
        meta: Optional[Meta] = None,
        **kwargs,
    ) -> None:
        # the "--chip" option in esptool, for beta chips, the target name and the name in esptool are different
        esptool_target = beta_target or target or 'auto'

        if esptool_target not in ['auto', *ESPTOOL_CHIPS]:
            raise ValueError(
                f'esptool version {ESPTOOL_VERSION} not support target {esptool_target}\n'
                f'Supported targets: {ESPTOOL_CHIPS}'
            )

        self._meta = meta
        self.esp_flash_force = esp_flash_force
        self.skip_autoflash = skip_autoflash
        self.flash_port = flash_port
        self._flashed_with_different_port = False

        self.erase_all = erase_all
        self.esptool_baud = esptool_baud

        self._before_init_port(msg_queue)

        # the "--chip" option in esptool, for beta chips, the target name and the name in esptool are different
        esptool_target = beta_target or target or 'auto'
        if esptool_target not in ['auto', *ESPTOOL_CHIPS]:
            raise ValueError(
                f'esptool version {ESPTOOL_VERSION} not support target {esptool_target}\n'
                f'Supported targets: {ESPTOOL_CHIPS}'
            )

        if port is None:  # auto detect port
            available_ports = esptool.get_port_list()
            ports = list(set(available_ports) - set(self.occupied_ports.keys()))

            # sort to make /dev/ttyS* ports before /dev/ttyUSB* ports
            # esptool will reverse the list
            ports.sort()
            if port_mac:
                for port in ports:
                    if _is_port_mac_verified(pexpect_proc, port, port_mac, msg_queue):
                        ports = [port]
                        break
                else:
                    raise ValueError(f'The specified MAC address {port_mac} cannot be found.')

            # prioritize the cache recorded target port
            if esptool_target and self._meta:
                ports.sort(key=lambda x: self._meta.hit_port_target_cache(x, esptool_target))

            logging.debug(f'Detecting ports from {", ".join(ports)}')
        else:
            if port_mac:
                if _is_port_mac_verified(pexpect_proc, port, port_mac, msg_queue):
                    ports = [port]
                else:
                    raise ValueError(f'The specified MAC address {port_mac} binds with different port, not with {port}')
            else:
                ports = [port]

        # normal loader
        with contextlib.redirect_stdout(msg_queue):
            self.esp = esptool.get_default_connected_device(
                ports,
                port=port,
                connect_attempts=3,
                initial_baud=baud,
                chip=esptool_target,
            )

        if not self.esp:
            raise ValueError('Couldn\'t auto detect chip. Please manually specify with "--port"')

        target = self.esp.CHIP_NAME.lower().replace('-', '')
        logging.info('Target: %s, Port: %s', target, self.esp.serial_port)

        self.target = target

        super().__init__(msg_queue=msg_queue, port=self.esp._port, baud=baud, meta=meta, **kwargs)

    def _before_init_port(self, q: MessageQueue):
        pass

    def _post_init(self):
        if self._meta:
            self._meta.set_port_target_cache(self.port, self.target)

        if self.erase_all and not self._flashed_with_different_port:
            esptool.main(['erase_flash'], esp=self.esp)

            if self._meta:
                self._meta.drop_port_app_cache(self.port)

        super()._post_init()

    def _start(self):
        self.hard_reset()

    def use_esptool(hard_reset_after: Optional[bool] = None, no_stub: Optional[bool] = None):
        """
        1. tell the redirect serial thread to stop reading from the `pyserial` instance
        2. esptool reuse the `pyserial` instance and call `esptool.main()` to do the actual work
        3. tell the redirect serial thread to continue reading from serial

        Args:
            hard_reset_after: run hard reset after (deprecated)
            no_stub: disable launching the flasher stub (deprecated)
        """
        if hard_reset_after is not None:
            warn(
                "The 'hard_reset_after' parameter is now read directly from `flasher_args.json` "
                'and does not need to be explicitly set. This parameter will be removed in 2.0 release.',
                DeprecationWarning,
            )

        if no_stub is not None:
            warn(
                "The 'no_stub' parameter is now read directly from `flasher_args.json` "
                'and does not need to be explicitly set. This parameter will be removed in 2.0 release.',
                DeprecationWarning,
            )

        def decorator(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                with self.disable_redirect_thread():
                    with contextlib.redirect_stdout(self._q):
                        settings = self.proc.get_settings()
                        self.esp.connect()
                        ret = func(self, *args, **kwargs)
                        self.proc.apply_settings(settings)
                return ret

            return wrapper

        return decorator

    def hard_reset(self):
        """Hard reset your espressif device"""
        self.esp.hard_reset()

    @use_esptool()
    def erase_flash(self, force: bool = False) -> None:
        """Erase the complete flash"""
        logging.info('Erasing the flash')
        options = ['erase_flash']

        if force or self.esp_flash_force:
            options.append('--force')

        esptool.main(options, esp=self.esp)

        if self._meta:
            self._meta.drop_port_app_cache(self.port)

    @property
    def stub(self):
        warn(
            'Please use `self.esp` instead of `self.stub`. `self.stub` will be removed in 2.0 release.',
            DeprecationWarning,
        )
        return self.esp

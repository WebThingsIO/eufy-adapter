"""Eufy adapter for Mozilla IoT Gateway."""

from gateway_addon import Adapter, Database
import lakeside

from .eufy_device import EufyBulb, EufySwitch


_TIMEOUT = 3


class EufyAdapter(Adapter):
    """Adapter for Eufy smart home devices."""

    def __init__(self, verbose=False):
        """
        Initialize the object.

        verbose -- whether or not to enable verbose logging
        """
        self.name = self.__class__.__name__
        Adapter.__init__(self,
                         'eufy-adapter',
                         'eufy-adapter',
                         verbose=verbose)

        self.username = None
        self.password = None

        database = Database(self.package_name)
        if database.open():
            config = database.load_config()

            if 'username' in config and len(config['username']) > 0:
                self.username = config['username']

            if 'password' in config and len(config['password']) > 0:
                self.password = config['password']

            database.close()

        self.pairing = False
        self.start_pairing(_TIMEOUT)

    def start_pairing(self, timeout):
        """
        Start the pairing process.

        timeout -- Timeout in seconds at which to quit pairing
        """
        if self.username is None or self.password is None:
            return

        self.pairing = True
        for dev in lakeside.get_devices(self.username, self.password):
            if not self.pairing:
                break

            _id = 'eufy-' + dev['address']  # TODO: this is unreliable
            if _id not in self.devices:
                address = dev['address']
                code = dev['code']
                model = dev['type']
                name = dev['name']

                if model in ['T1201', 'T1202', 'T1211']:
                    eufy_dev = lakeside.switch(address, code, model)
                    device = EufySwitch(self, _id, name, eufy_dev)
                elif model in ['T1011', 'T1012', 'T1013']:
                    eufy_dev = lakeside.bulb(address, code, model)
                    device = EufyBulb(self, _id, name, eufy_dev)
                else:
                    continue

                self.handle_device_added(device)

    def cancel_pairing(self):
        """Cancel the pairing process."""
        self.pairing = False

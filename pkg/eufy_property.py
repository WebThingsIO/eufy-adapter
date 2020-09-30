"""Eufy adapter for WebThings Gateway."""

from gateway_addon import Property

from .util import kelvin_to_relative_temp


class EufyProperty(Property):
    """Eufy property type."""

    def __init__(self, device, name, description, value):
        """
        Initialize the object.

        device -- the Device this property belongs to
        name -- name of the property
        description -- description of the property, as a dictionary
        value -- current value of this property
        """
        Property.__init__(self, device, name, description)
        self.set_cached_value(value)

    def set_state(self, **kwargs):
        """
        Set the current value of the property.

        value -- the value to set
        """
        try:
            self.device.eufy_dev.set_state(**kwargs)
        except BrokenPipeError:
            try:
                self.device.eufy_dev.connect()
            except OSError:
                return

            self.device.eufy_dev.set_state(**kwargs)


class EufySwitchProperty(EufyProperty):
    """Property type for Eufy smart switches/plugs."""

    def set_value(self, value):
        """
        Set the current value of the property.

        value -- the value to set
        """
        if self.name != 'on':
            return

        self.set_state(power=value)
        self.set_cached_value(value)
        self.device.notify_property_changed(self)

    def update(self):
        """Update the current value, if necessary."""
        if self.name != 'on':
            return

        value = self.device.is_on()
        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)


class EufyBulbProperty(EufyProperty):
    """Property type for Eufy smart bulbs."""

    def set_value(self, value):
        """
        Set the current value of the property.

        value -- the value to set
        """
        color_mode_prop = None
        if 'colorMode' in self.device.properties:
            color_mode_prop = self.device.properties['colorMode']

        if self.name == 'on':
            self.set_state(power=value)
        elif self.name == 'color':
            self.set_state(colors=[int(value[1:3], 16),
                                   int(value[3:5], 16),
                                   int(value[5:7], 16)])

            # update the colorMode property
            if color_mode_prop is not None:
                color_mode_prop.set_cached_value('color')
                self.device.notify_property_changed(color_mode_prop)
        elif self.name == 'level':
            self.set_state(brightness=value)
        elif self.name == 'colorTemperature':
            value = max(value, self.description['minimum'])
            value = min(value, self.description['maximum'])
            self.set_state(temperature=kelvin_to_relative_temp(value))

            # update the colorMode property
            if color_mode_prop is not None:
                color_mode_prop.set_cached_value('temperature')
                self.device.notify_property_changed(color_mode_prop)
        else:
            return

        self.set_cached_value(value)
        self.device.notify_property_changed(self)

    def update(self):
        """Update the current value, if necessary."""
        if self.name == 'on':
            value = self.device.is_on()
        elif self.name == 'color':
            value = self.device.color()
        elif self.name == 'level':
            value = self.device.brightness()
        elif self.name == 'colorTemperature':
            value = self.device.color_temp()
        elif self.name == 'colorMode':
            value = self.device.color_mode()
        else:
            return

        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)

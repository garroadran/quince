"""Entry widgets that support validation"""

import tkinter as tk


def select_all(event):
    """Select all callback for the Entry widget

    Args:
        event - Tkinter binding event
    """
    event.widget.select_range(0, "end")
    event.widget.icursor("end")
    return "break"


class ValidatingEntry(tk.Entry):
    """Base class for entry widgets that can be validated"""

    def __init__(self, master, value="", **kw):
        tk.Entry.__init__(self, master, **kw)
        self.__value = value
        self.__variable = tk.StringVar()
        self.__variable.set(value)
        self.config(textvariable=self.__variable)
        self.default_bg = self.cget("background")
        self._trace_id = None
        self.bind("<Control-a>", select_all)

    def __callback(self, *dummy):
        self.config(bg=self.default_bg)
        self.__variable.trace_vdelete("w", self._trace_id)

    def validate(self):
        """Throws a warning for the user if validation fails."""
        valid = self._validator(self.__variable.get())

        if valid:
            return True

        self._trace_id = self.__variable.trace("w", self.__callback)
        self.config(bg="light salmon")
        return False

    def _validator(self, value):
        raise NotImplementedError("Subclasses must override \
                                   the _validator method.")


# pylint: disable=no-member, access-member-before-definition
class UserNameEntry(ValidatingEntry):
    """Entry field with validation for user names"""
    def __init__(self, master, value="", *args, **kwargs):
        """
        Args:
            master (tkinter widget) - Root node
            value (string) - Default text to put in the entry box

        Kwargs:
            char_limit (int) - Number of chars at which input gets cut off
        """
        self.char_limit = kwargs.get("char_limit")
        kwargs.pop("char_limit", None)

        ValidatingEntry.__init__(self, master, value, *args, **kwargs)
        self._ValidatingEntry__variable.trace("w", self._maxcharlimit)

    def _maxcharlimit(self, *dummy):
        value = self._ValidatingEntry__variable.get()

        if self.char_limit is not None and len(value) > self.char_limit:
            self._ValidatingEntry__variable.set(self._ValidatingEntry__value)
        else:
            self._ValidatingEntry__value = value

    def _validator(self, value):
        """
        Args:
            value (string) - Entry text to validate
        """
        if len(value) > 12 or value is None or value == "":
            return False

        return True

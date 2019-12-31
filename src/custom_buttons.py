"""
Contains customized buttons

Available classes:
--------------
    - `DropBtn`
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

from kivymd.uix.button import MDRaisedButton


class DropBtn(MDRaisedButton):
    """
    A customized `MDRaisedButton` to be used in `DropDowns`

    method:
    -------
        `select`:
            Action to be taken when this button is selected
    """

    def select(self, instance):
        """
        parameters
        ----------
            `instance`: instance of the dropdown button its been attached to
            Override this method as per requirements of a dropdown
        """
        pass

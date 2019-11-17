"""
This file contains different customized `DropDown`s

Availabe classes:
-----------------
    - CourseDrop
    - StreamDrop
    - CourseDropFee
    - StreamDropFee
    - CatagoryDrop

"""

from kivy.uix.dropdown import DropDown

__all__ = (
    "CourseDrop",
    "StreamDrop",
    "CatagoryDrop",
    "CourseDropFee",
    "StreamDropFee",
)

class CourseDrop(DropDown):
    """
    `DropDown` to select a course from a list of available courses
    """
    pass


class StreamDrop(DropDown):
    """
    `DropDown` to select a stream from a list of available streams
    """
    pass


class CourseDropFee(DropDown):
    """
    `DropDown` to select a course from a list of available courses in the `generate_receipt` screen

    Two different dropdowns for course 'cause this class will have some additional functionalities
    """
    pass


class StreamDropFee(DropDown):
    """
    `DropDown` to select a stream from a list of available streams in the `generate_receipt` screen

    Two different dropdowns for streams 'cause this class will have some additional functionalities
    """
    pass


class CatagoryDrop(DropDown):
    """
    `DropDown` to select a category in the `generate_receipt` screen
    Currently categories available are `All` and `Due`
    """
    pass

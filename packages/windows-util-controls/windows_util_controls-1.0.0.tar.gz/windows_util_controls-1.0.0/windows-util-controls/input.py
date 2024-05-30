"""
User-simple and friendly input functions for PyAutoGUI.

This module provides a set of functions that wrap around PyAutoGUI's functions

Functions:
    type: Types a string into the active window.
    mousepos: Moves the mouse to the specified position.

"""


import pyautogui
import math


class Easings:
    @staticmethod
    def linear(t):
        """
        Linear easing function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return t

    @staticmethod
    def ease_in_quad(t):
        """
        Quadratic ease-in function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return t * t

    @staticmethod
    def ease_out_quad(t):
        """
        Quadratic ease-out function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return t * (2 - t)

    @staticmethod
    def ease_in_out_quad(t):
        """
        Quadratic ease-in-out function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        if t < 0.5:
            return 2 * t * t
        else:
            return -1 + (4 - 2 * t) * t

    @staticmethod
    def ease_in_cubic(t):
        """
        Cubic ease-in function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return t * t * t

    @staticmethod
    def ease_out_cubic(t):
        """
        Cubic ease-out function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return (t - 1)**3 + 1

    @staticmethod
    def ease_in_out_cubic(t):
        """
        Cubic ease-in-out function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        if t < 0.5:
            return 4 * t * t * t
        else:
            return (t - 1) * (2 * t - 2) * (2 * t - 2) + 1

    @staticmethod
    def ease_in_quart(t):
        """
        Quartic ease-in function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return t * t * t * t

    @staticmethod
    def ease_out_quart(t):
        """
        Quartic ease-out function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return 1 - (t - 1)**4

    @staticmethod
    def ease_in_out_quart(t):
        """
        Quartic ease-in-out function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        if t < 0.5:
            return 8 * t * t * t * t
        else:
            return 1 - 8 * (t - 1)**4

    @staticmethod
    def ease_in_quint(t):
        """
        Quintic ease-in function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return t * t * t * t * t

    @staticmethod
    def ease_out_quint(t):
        """
        Quintic ease-out function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return 1 + (t - 1)**5

    @staticmethod
    def ease_in_out_quint(t):
        """
        Quintic ease-in-out function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        if t < 0.5:
            return 16 * t * t * t * t * t
        else:
            return 1 + 16 * (t - 1)**5

    @staticmethod
    def ease_in_sine(t):
        """
        Sine ease-in function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return 1 - math.cos((t * math.pi) / 2)

    @staticmethod
    def ease_out_sine(t):
        """
        Sine ease-out function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return math.sin((t * math.pi) / 2)

    @staticmethod
    def ease_in_out_sine(t):
        """
        Sine ease-in-out function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return -(math.cos(math.pi * t) - 1) / 2

    @staticmethod
    def ease_in_expo(t):
        """
        Exponential ease-in function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return 0 if t == 0 else 2**(10 * (t - 1))

    @staticmethod
    def ease_out_expo(t):
        """
        Exponential ease-out function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return 1 if t == 1 else 1 - 2**(-10 * t)

    @staticmethod
    def ease_in_out_expo(t):
        """
        Exponential ease-in-out function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        if t == 0:
            return 0
        if t == 1:
            return 1
        if t < 0.5:
            return 2**(10 * (2 * t - 1)) / 2
        else:
            return (2 - 2**(-10 * (2 * t - 1))) / 2

    @staticmethod
    def ease_in_circ(t):
        """
        Circular ease-in function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return 1 - math.sqrt(1 - t * t)

    @staticmethod
    def ease_out_circ(t):
        """
        Circular ease-out function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        return math.sqrt(1 - (t - 1)**2)

    @staticmethod
    def ease_in_out_circ(t):
        """
        Circular ease-in-out function.
        
        :param t: A float between 0 and 1 representing the normalized time.
        :return: A float representing the eased value.
        """
        if t < 0.5:
            return (1 - math.sqrt(1 - 4 * t * t)) / 2
        else:
            return (math.sqrt(1 - (2 * t - 2)**2) + 1) / 2

# region Inputs
def type(text):
    pyautogui.typewrite(text)
    
def mousepos(x, y, duration, tween):
    pyautogui.moveTo(x=x, y=y, duration=duration, tween=tween)
    
def clickCursorLeft():
    pyautogui.click()
    
def clickCursorRight():
    pyautogui.rightClick()

def clickCursorMiddle():
    pyautogui.middleClick()
    
def clickCursorLeftDouble():
    pyautogui.doubleClick()
    
def clickCursorLeftTriple():
    pyautogui.tripleClick()
    
def clickCursorTimesLeft(times):
    for i in range(times):
        pyautogui.click()

def clickCursorTimesRight(times):
    for i in range(times):
        pyautogui.rightClick()
        
def clickCursorTimesMiddle(times):
    for i in range(times):
        pyautogui.middleClick()
def clickCursorTimesDouble(times):
    for i in range(times):
        pyautogui.doubleClick()
def clickCursorTimesTriple(times):
    for i in range(times):
        pyautogui.tripleClick()

def drag(x, y, duration, tween):
    pyautogui.dragTo(x=x, y=y, duration=duration, tween=tween)
    
def dragRel(xOffset, yOffset, duration, tween):
    pyautogui.dragRel(xOffset=xOffset, yOffset=yOffset, duration=duration, tween=tween)
# endregion
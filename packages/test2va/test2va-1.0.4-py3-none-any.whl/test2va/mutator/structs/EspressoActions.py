from appium.webdriver import WebElement
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver

from ...parser.types.LibTypes import ActionData


class EspressoActions:
    @staticmethod
    def click(element: WebElement, _action: ActionData, _driver: WebDriver):
        element.click()

    @staticmethod
    def close_soft_keyboard(_element: WebElement, action: ActionData, driver: WebDriver):
        driver.hide_keyboard()

    @staticmethod
    def long_click(element: WebElement, _action: ActionData, driver: WebDriver):
        actions = TouchAction(driver)
        actions.long_press(element).release().perform()

    @staticmethod
    def press_ime_action_button(element: WebElement, action: ActionData, driver: WebDriver):
        driver.press_keycode(66)

    @staticmethod
    def press_back(element: WebElement, action: ActionData, driver: WebDriver):
        driver.press_keycode(4)

    @staticmethod
    def replace_text(element: WebElement, action: ActionData, driver: WebDriver):
        element.clear()
        element.send_keys(action["args"][0]["content"])

    @staticmethod
    def type_text(element: WebElement, action: ActionData, driver: WebDriver):
        element.send_keys(action["args"][0]["content"])

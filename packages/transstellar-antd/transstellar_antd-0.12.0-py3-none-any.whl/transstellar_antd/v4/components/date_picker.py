from ...components import DatePicker as BaseDatePicker


class DatePicker(BaseDatePicker):
    XPATH_CURRENT = '//div[contains(@class, "ant-picker")]'

import re
from .constants import CN_DECIMAL_4S_UNITS, EN_DECIMAL_3S_UNITS, CN_INTEGER_0_TO_9, CN_DECIMAL_UNITS, CN_POINT_NAME, \
    CN_MINUS, CN_CURRENCY_UNIT, CN_POINTS_UNITS, CN_ONLY_NAME, CN_CNY_NAME, CN_USD_NAME, CN_EUR_NAME, EN_INTEGER_0_TO_9, \
    EN_INTEGER_1NS, EN_INTEGER_2NS, EN_HUNDRED_NAME, EN_POINT_NAME, EN_MINUS, EN_POINTS_UNITS, EN_CNY_NAME, EN_USD_NAME, \
    EN_EUR_NAME, EN_ONLY_NAME, EN_AND_NAME


class Digital(float):
    def __new__(cls, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"输入变量必须为整形或浮点型: {value}")
        return super().__new__(cls, value)

    def __init__(self, value):
        self._decimal_string = None
        self._integer_string = None
        self._ten_thousands_breaks = None
        self._thousands_breaks = None
        self._capital_cn_decimal = None
        self._capital_cn_integer = None
        self._capital_cn = None
        self._capital_cn_currency = None
        self._capital_cn_cny = None
        self._capital_cn_usd = None
        self._capital_cn_eur = None
        self._capital_en_decimal = None
        self._capital_en_integer = None
        self._capital_en = None
        self._capital_en_currency_decimal = None
        self._capital_en_currency_integer = None
        self._capital_en_currency = None
        self._capital_en_cny = None
        self._capital_en_usd = None
        self._capital_en_eur = None

    def __str__(self):
        return super().__str__()

    def is_integer(self):
        return isinstance(self, int)

    def is_float(self):
        return isinstance(self, int)

    def to_integer(self):
        return int(self)

    def to_float(self):
        return float(self)

    @property
    def string(self):
        return str(self)

    def is_negative(self):
        return self < 0

    def is_positive(self):
        return self > 0

    @property
    def decimal_string(self):
        if self._decimal_string is None:
            match = re.search(r'\.(\d+)', self.string)
            if match:
                self._decimal_string = match.group(1)
            else:
                self._decimal_string = '0'
        return self._decimal_string

    @property
    def integer_string(self):
        if self._integer_string is None:
            self._integer_string = str(self.to_integer())
        return self._integer_string

    @property
    def ten_thousands_breaks(self):
        if self._ten_thousands_breaks is None:
            self._ten_thousands_breaks = []
            for i in range(len(self.integer_string), 0, -4):
                self._ten_thousands_breaks.append(self.integer_string[max(i - 4, 0):i])
            # 分组正向
            self._ten_thousands_breaks.reverse()
            # 第一组不足4位时在前面用0补齐
            self._ten_thousands_breaks[0] = f"{self._ten_thousands_breaks[0]:0>4}"
        return self._ten_thousands_breaks

    @property
    def thousands_breaks(self):
        if self._thousands_breaks is None:
            self._thousands_breaks = []
            for i in range(len(self.integer_string), 0, -3):
                self._thousands_breaks.append(self.integer_string[max(i - 3, 0):i])
            # 分组正向
            self._thousands_breaks.reverse()
            # 第一组不足3位时在前面用0补齐
            self._thousands_breaks[0] = f"{self._thousands_breaks[0]:0>3}"
        return self._thousands_breaks

    @property  # 数字小数中文大写
    def capital_cn_decimal(self):
        if self._capital_cn_decimal is None:
            self._capital_cn_decimal = ''
            for i in range(0, len(self.decimal_string)):
                self._capital_cn_decimal += CN_INTEGER_0_TO_9[int(self.decimal_string[i])]
            if self._capital_cn_decimal == CN_INTEGER_0_TO_9[0]:
                self._capital_cn_decimal = ''
        return self._capital_cn_decimal

    def _capital_cn_by_ten_thousands_breaks_number(self, group_serial, number_serial):
        # 从万分位分组中取数字转为中文大写
        capital = f'{CN_INTEGER_0_TO_9[int(self.ten_thousands_breaks[group_serial][number_serial])]}'
        if self.ten_thousands_breaks[group_serial][number_serial] != '0' and number_serial < 3:
            capital += f'{CN_DECIMAL_UNITS[2 - number_serial]}'
        return capital

    @property  # 数字整数中文大写
    def capital_cn_integer(self):
        if self._capital_cn_integer is None:
            # 设定前面判断字符是不是非0
            first_zero = True
            last_zero = False
            self._capital_cn_integer = ''
            groups_quantity = len(self.ten_thousands_breaks)
            for group_serial in range(0, groups_quantity):
                capitals = ''
                group = self.ten_thousands_breaks[group_serial]
                for number_serial in range(4):
                    if group[number_serial] != '0':
                        if last_zero and not first_zero:
                            capitals += CN_INTEGER_0_TO_9[0]
                        capitals += self._capital_cn_by_ten_thousands_breaks_number(group_serial, number_serial)
                        first_zero = False
                        last_zero = False
                    else:
                        last_zero = True
                self._capital_cn_integer += capitals
                if group_serial < groups_quantity - 1:
                    self._capital_cn_integer += \
                        f'{CN_DECIMAL_4S_UNITS[groups_quantity - group_serial - 2]}'
            if not self._capital_cn_integer:
                self._capital_cn_integer = CN_INTEGER_0_TO_9[0]
        return self._capital_cn_integer

    @property  # 数字中文大写
    def capital_cn(self):
        if self._capital_cn is None:
            self._capital_cn = self.capital_cn_integer
            if self.capital_cn_decimal != '':
                self._capital_cn += CN_POINT_NAME + self.capital_cn_decimal
            if self.is_negative():
                self._capital_cn = f'{CN_MINUS} ' + self._capital_cn
        return self._capital_cn

    @property  # 货币中文大写
    def capital_cn_currency(self):
        if self._capital_cn_currency is None:
            self._capital_cn_currency = self.capital_cn_integer + CN_CURRENCY_UNIT
            decimal_cn = ''
            if len(self.decimal_string) > 0:
                if len(self.decimal_string) > 2 and self.decimal_string[2] != '0':
                    decimal_cn = CN_INTEGER_0_TO_9[int(self.decimal_string[2])] + CN_POINTS_UNITS[2]
                if len(self.decimal_string) > 1 and not (self.decimal_string[1] == '0' and decimal_cn == ''):
                    decimal_cn = CN_INTEGER_0_TO_9[int(self.decimal_string[1])] + CN_POINTS_UNITS[1] + decimal_cn
                if not (self.decimal_string[0] == '0' and decimal_cn == ''):
                    decimal_cn = CN_INTEGER_0_TO_9[int(self.decimal_string[0])] + CN_POINTS_UNITS[0] + decimal_cn
                self._capital_cn_currency += decimal_cn
            if not decimal_cn:
                self._capital_cn_currency += CN_ONLY_NAME
        return self._capital_cn_currency

    @property  # 数字中文大写
    def capital_cn_cny(self):
        if self._capital_cn_cny is None:
            self._capital_cn_cny = CN_CNY_NAME + self.capital_cn_currency
        return self._capital_cn_cny

    @property  # 数字中文大写
    def capital_cn_usd(self):
        if self._capital_cn_usd is None:
            self._capital_cn_usd = CN_USD_NAME + self.capital_cn_currency
        return self._capital_cn_usd

    @property  # 数字中文大写
    def capital_cn_eur(self):
        if self._capital_cn_eur is None:
            self._capital_cn_eur = CN_EUR_NAME + self.capital_cn_currency
        return self._capital_cn_eur

    @property  # 数字小数英文大写
    def capital_en_decimal(self):
        if self._capital_en_decimal is None:
            data = []
            for i in range(0, len(self.decimal_string)):
                data.append(EN_INTEGER_0_TO_9[int(self.decimal_string[i])])
            self._capital_en_decimal = ' '.join(data)
        return self._capital_en_decimal

    def _capital_en_by_thousands_breaks_add_and(self, group_serial, number_serial):
        g = self.thousands_breaks[group_serial]
        for i in range(number_serial + 1, 2):
            if g[i] != '0':
                return True
        if group_serial < len(self.thousands_breaks) - 1:
            for i in range(group_serial + 1, len(self._decimal_string)):
                for j in self.thousands_breaks[i]:
                    if j != 0:
                        return True
        return False

    def _capital_en_by_thousands_breaks(self, group_serial):
        g = self.thousands_breaks[group_serial]
        caps = []
        if g[0] != '0':
            caps.append(EN_INTEGER_0_TO_9[int(g[0])])
            caps.append(EN_HUNDRED_NAME)
            if self._capital_en_by_thousands_breaks_add_and(group_serial, 0):
                caps.append(EN_AND_NAME)
            caps.extend(self._capital_en_by_thousands_breaks_2(group_serial))
        else:
            caps.extend(self._capital_en_by_thousands_breaks_2(group_serial))
        return caps

    def _capital_en_by_thousands_breaks_2(self, group_serial):
        g = self.thousands_breaks[group_serial]
        caps = []
        if int(g[1]) >= 2:
            caps.append(EN_INTEGER_2NS[int(g[1]) - 2])
            caps.extend(self._capital_en_by_thousands_breaks_1(group_serial))
        elif g[1] == '1':
            caps.append(EN_INTEGER_1NS[int(g[2])])
        else:
            caps.extend(self._capital_en_by_thousands_breaks_1(group_serial))
        return caps

    def _capital_en_by_thousands_breaks_1(self, group_serial):
        g = self.thousands_breaks[group_serial]
        caps = []
        if g[2] != '0':
            caps.append(EN_INTEGER_0_TO_9[int(g[2])])
        return caps

    @property  # 数字整数英文大写
    def capital_en_integer(self):
        if self._capital_en_integer is None:
            groups_quantity = len(self.thousands_breaks)
            caps = []
            for i in range(0, len(self.thousands_breaks)):
                caps.extend(self._capital_en_by_thousands_breaks(i))
                if i < groups_quantity - 1:
                    caps.append(EN_DECIMAL_3S_UNITS[groups_quantity - i - 2])
            self._capital_en_integer = ' '.join(caps)
            if not self._capital_en_integer:
                self._capital_en_integer = EN_INTEGER_0_TO_9[0]
        return self._capital_en_integer

    @property  # 数字英文大写
    def capital_en(self):
        if self._capital_en is None:
            self._capital_en = self.capital_en_integer
            if self.capital_en_decimal != '' and self.capital_en_decimal != EN_INTEGER_0_TO_9[0]:
                self._capital_en += f' {EN_POINT_NAME} {self.capital_en_decimal}'
            if self.is_negative():
                self._capital_en = f'{EN_MINUS} ' + self._capital_en
        return self._capital_en

    @property  # 货币中文大写
    def capital_en_currency(self):
        if self._capital_en_currency is None:
            self._capital_en_currency = self.capital_en_integer
            ds = []
            if len(self.decimal_string) > 0:
                if len(self.decimal_string) > 2 and self.decimal_string[2] != '0':
                    ds.append(EN_POINTS_UNITS[2] if int(self.decimal_string[2]) in [0, 1] else f'{EN_POINTS_UNITS[2]}s')
                    ds.append(EN_INTEGER_0_TO_9[int(self.decimal_string[2])])
                if len(self.decimal_string) > 1 and not (self.decimal_string[1] == '0' and len(ds) <= 0):
                    ds.append(EN_POINTS_UNITS[1] if int(self.decimal_string[1]) in [0, 1] else f'{EN_POINTS_UNITS[1]}s')
                    ds.append(EN_INTEGER_0_TO_9[int(self.decimal_string[1])])
                if not (self.decimal_string[0] == '0' and len(ds) <= 0):
                    ds.append(EN_POINTS_UNITS[0] if int(self.decimal_string[0]) in [0, 1] else f'{EN_POINTS_UNITS[0]}s')
                    ds.append(EN_INTEGER_0_TO_9[int(self.decimal_string[0])])
                if len(ds) > 0:
                    ds.reverse()
                    self._capital_en_currency += f' {EN_AND_NAME} ' + ' '.join(ds)
                else:
                    self._capital_en_currency += f' {EN_ONLY_NAME}'
        return self._capital_en_currency

    @property
    def capital_en_cny(self):
        if self._capital_en_cny is None:
            self._capital_en_cny = f'{EN_CNY_NAME} {self.capital_en_currency}'
        return self._capital_en_cny

    @property
    def capital_en_usd(self):
        if self._capital_en_usd is None:
            self._capital_en_usd = f'{EN_USD_NAME} {self.capital_en_currency}'
        return self._capital_en_usd

    @property
    def capital_en_eur(self):
        if self._capital_en_eur is None:
            self._capital_en_eur = f'{EN_EUR_NAME} {self.capital_en_currency}'
        return self._capital_en_eur

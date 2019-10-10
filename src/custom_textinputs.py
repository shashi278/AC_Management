from kivy.uix.textinput import TextInput

from kivymd.uix.textfield import MDTextField


class DateInput(MDTextField):

    dd = ""
    mm = ""
    yyyy = ""

    def date_filter(self, substring, do_undo):
        print(substring)

        try:
            text = str(int(substring))
            # print("self.text: "+self.text+text)
            # print("cursor: {}".format(self.cursor[0]))

            if self.cursor[0] == 0:
                if not len(self.text):
                    self.dd = ""
                    self.dd += text
                    return text

                elif self.text[0] == "-":
                    self.dd = text
                    return text

                elif len(self.text) >= 2 and self.text[1] == "-":
                    self.dd = text + self.dd[1]
                    return text

                elif len(self.dd) == 1:
                    self.dd = text + self.dd
                    self.text = self.text + "-"
                    self.cursor = (0, 0)
                    return text

                elif len(self.dd) > len(self.text):
                    self.dd = self.dd[0] + text
                    self.text = self.text + "-"
                    self.cursor = (0, 0)
                    return text

                    # elif len(self.mm)==2 and len(self.yyyy)==4:
                    # if self.text[0]=='-':
                    return ""

            if self.cursor[0] == 1:
                if len(self.dd) == 1 and len(self.text) == 1:
                    self.dd += text
                    return text + "-"
                elif len(self.dd) > len(self.text):
                    self.dd = self.dd[0] + text
                    return text + "-"
                else:
                    if self.text[1] == "-":
                        self.dd = self.dd[0] + text
                        return text
                    else:
                        return ""

            if self.cursor[0] == 2:
                if len(self.text) == 2:
                    return "-"
                else:
                    return "-"

            if self.cursor[0] == 3:
                if len(self.text) == 3:
                    self.mm = ""
                    self.mm += text
                    return text
                elif len(self.mm) == 2:
                    self.mm = text + self.mm[1]
                    return text
                elif self.text[3] == "-":
                    self.mm = text
                    return text
                elif len(self.mm) == 1:
                    self.mm = text + self.mm
                    self.text = self.text + "-"
                    self.cursor = (3, 0)
                    return text

            if self.cursor[0] == 4:
                if len(self.text) == 4:
                    if len(self.mm) == 2:
                        self.mm = self.mm[0] + text
                    else:
                        self.mm += text
                    return text + "-"
                elif self.text[4] == "-":
                    self.mm = self.mm[0] + text
                    return text

            if self.cursor[0] == 5:
                if len(self.text) == 5:
                    return "-"
                else:
                    return "-"

            if self.cursor[0] > 5 and len(self.text) != 10:
                self.yyyy += text
                return text
            else:
                return ""

        except Exception as e:
            print(e)
            return ""


class TextInputForList(TextInput):
    pass

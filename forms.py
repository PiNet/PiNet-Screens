from wtforms import Form, StringField, TextAreaField


class ClientForm(Form):
    mac_address = StringField("MAC Address")
    hostname = StringField("Machine hostname")
    location = StringField("Machine location")


class BrowserContentForm(Form):
    content_name = StringField("Content name")
    content_url = StringField("URL")


class ScriptContentForm(Form):
    content_name = StringField("Content name")
    content_script = TextAreaField("Bash script content")

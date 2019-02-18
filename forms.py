from wtforms import Form, StringField

class ClientForm(Form):
    mac_address = StringField("MAC Address")
    hostname = StringField("Machine hostname")
    location = StringField("Machine location")
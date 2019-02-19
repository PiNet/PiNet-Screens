from wtforms import Form, StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, MacAddress, ValidationError, URL


class LoginForm(Form):
    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])


class ClientForm(Form):
    def hostname_validation(form, field):
        if not "." in field.data or len(field.data) > 63:
            raise ValidationError('Hostname must be in the format of name.something and be under 63 chars long.')

    def pi_validation(form, field):
        if not field.data.lower().startswith("b8:27:eb"):
            raise ValidationError('Invalid client MAC address. All Raspberry Pi MAC addresses start with B8:27:EB')

    mac_address = StringField("MAC Address", validators=[DataRequired(), MacAddress(), pi_validation])
    hostname = StringField("Machine hostname", validators=[DataRequired(), hostname_validation])
    location = StringField("Machine location", validators=[DataRequired()])


class BrowserContentForm(Form):
    content_name = StringField("Content name", [DataRequired()])
    content_url = StringField("URL", [DataRequired(), URL()])


class ScriptContentForm(Form):
    content_name = StringField("Content name", [DataRequired()])
    content_script = TextAreaField("Bash script content", [DataRequired()])

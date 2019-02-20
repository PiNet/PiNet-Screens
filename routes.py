from flask import Blueprint, render_template, request, make_response, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user

import forms
import lts_conf
import database
import util
import secrets.config as config


routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route("/login", methods=['GET', 'POST'])
def login():

    form = forms.LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        status, user = util.validate_login(username, password)
        if status:
            login_user(user)
            return redirect(url_for("routes.clients_home"))
        else:
            flash("Login failed - Credentials incorrect.", "danger")
            return render_template("login.html", form=form)
    return render_template("login.html", next=next, form=form)


@routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.login'))


@routes.route("/clients",  methods=['GET', 'POST'])
@routes.route("/clients/edit/<client_id>",  methods=['GET', 'POST'])
@login_required
def clients_home(client_id=None):
    form = forms.ClientForm(request.form)
    if request.method == 'POST' and form.validate():
        if not database.create_client(mac_address=form.mac_address.data, location=form.location.data, hostname=form.hostname.data, client_id=client_id):
            flash("Unable to add/edit, MAC address or hostname not unique.", "danger")
        else:
            flash("Client entry added/updated successfully.", "success")
            return redirect(url_for("routes.clients_home"))

    if client_id and request.method == "GET":
        client = database.get_client_from_id(int(client_id))
        form.mac_address.default = client.mac_address
        form.hostname.default = client.hostname
        form.location.default = client.location
        form.process()
    content = database.get_all_content()
    clients = database.get_all_clients()
    return render_template("clients_home.html", form=form, clients=clients, content=content, edit=bool(client_id))


@routes.route("/clients/disable_auto_login/<client_id>")
@login_required
def disable_auto_login(client_id):
    database.update_ldm_autologin(client_id, False)
    return redirect(url_for("routes.clients_home"))


@routes.route("/clients/enable_auto_login/<client_id>")
@login_required
def enable_auto_login(client_id):
    database.update_ldm_autologin(client_id, True)
    return redirect(url_for("routes.clients_home"))


@routes.route("/content")
@login_required
def content_home():
    browser_content = database.get_all_browser_content()
    script_content = database.get_all_script_content()
    return render_template("content_home.html", browser_content=browser_content, script_content=script_content)


@routes.route("/content/add_browser_content",  methods=['GET', 'POST'])
@login_required
def add_browser_content():
    form = forms.BrowserContentForm(request.form)
    if request.method == 'POST' and form.validate():
        if not database.create_content(content_name=form.content_name.data, browser=True, url=form.content_url.data):
            flash("Failed to add content. {} already exists.".format(form.content_name.data), "danger")
        return redirect(url_for("routes.content_home"))
    return render_template("add_browser_content.html", form=form)


@routes.route("/content/add_script_content",  methods=['GET', 'POST'])
@login_required
def add_script_content():
    form = forms.ScriptContentForm(request.form)
    if request.method == 'POST' and form.validate():
        if not database.create_content(content_name=form.content_name.data, script=True, script_body=form.content_script.data):
            flash("Failed to add content. {} already exists.".format(form.content_name.data), "danger")
        return redirect(url_for("routes.content_home"))
    return render_template("add_script_content.html", form=form)


@routes.route("/content/view_script/<content_id>")
@login_required
def view_script_content(content_id):
    content = database.get_content_from_id(content_id)
    return content.script_body


@routes.route("/content/remove/<content_id>")
@login_required
def remove_content(content_id):
    database.remove_content_from_id(content_id)
    flash("Content successfully removed.", "success")
    return redirect(url_for("routes.content_home"))


@routes.route("/clients/update_content_ajax", methods=['GET', 'POST'])
@login_required
def client_update_content_ajax():
    content_id = request.form['content_id']
    client_id = request.form['client_id']
    database.update_client_content(client_id, content_id)
    print("{} - {}".format(content_id, client_id))
    return ""


@routes.route("/clients/remove/<client_id>")
@login_required
def remove_client(client_id):
    database.remove_client_from_id(client_id)
    flash("Client successfully removed.", "success")
    return redirect(url_for("routes.clients_home"))


@routes.route("/clients/apply")
@login_required
def apply_config_update():
    util.build_scripts()

    flash("Updates applied to configuration files. Please reboot any edited clients if they do not automatically.", "success")
    return redirect(url_for("routes.clients_home"))


@routes.route("/endpoint/update", methods=['POST'])
def endpoint_update():
    update = request.json
    mac_address = update["mac_address"]
    hostname = update["hostname"]
    clients = database.get_all_clients()
    for client in clients:
        if client.mac_address == mac_address:
            database.update_client_check_in(client.client_id)
            return ""
    client_id = database.create_client(mac_address=mac_address, hostname=hostname, location="Unknown - Auto added")
    database.update_client_check_in(client_id)

    print(update)
    return ""
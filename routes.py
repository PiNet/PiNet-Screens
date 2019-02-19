from flask import Blueprint, render_template, request, make_response, redirect, flash, url_for

import forms
import lts_conf
import database

lts_conf_path = "test_data/lts.conf"

routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route("/clients",  methods=['GET', 'POST'])
@routes.route("/clients/edit/<client_mac>",  methods=['GET', 'POST'])
def clients_home(client_mac=None):
    form = forms.ClientForm(request.form)
    lts = lts_conf.LtsConf(lts_conf_path)
    #clients = lts.raspberry_pis
    clients = database.get_all_clients()
    if request.method == 'POST' and form.validate():
        database.create_client(mac_address=form.mac_address.data, location=form.location.data, hostname=form.hostname.data)
        #lts.add_update_client(mac_address=form.mac_address.data, location=form.location.data, hostname=form.hostname.data)
    if client_mac and request.method == "GET":
        client = lts.get_client(client_mac)
        form.mac_address.default = client.mac_address
        form.hostname.default = client.hostname
        form.location.default = client.location
        form.process()

    content = database.get_all_content()
    return render_template("clients_home.html", form=form, clients=clients, content=content)


@routes.route("/clients/disable_auto_login/<client_id>")
def disable_auto_login(client_id):
    lts = lts_conf.LtsConf(lts_conf_path)
    clients = database.get_all_clients()
    #clients = lts.raspberry_pis
    for client in clients:
        if client.client_id == client_id:
            client.ldm_autologin = False
            lts.write_conf()
            return redirect(url_for("routes.clients_home"))


@routes.route("/clients/enable_auto_login/<client_id>")
def enable_auto_login(client_id):
    lts = lts_conf.LtsConf(lts_conf_path)
    #clients = lts.raspberry_pis
    clients = database.get_all_clients()
    for client in clients:
        if client.client_id == client_id:
            client.ldm_autologin = True
            lts.write_conf()
            return redirect(url_for("routes.clients_home"))


@routes.route("/content")
def content_home():
    browser_content = database.get_all_browser_content()
    script_content = database.get_all_script_content()
    return render_template("content_home.html", browser_content=browser_content, script_content=script_content)


@routes.route("/content/add_browser_content",  methods=['GET', 'POST'])
def add_browser_content():
    form = forms.BrowserContentForm(request.form)
    if request.method == 'POST' and form.validate():
        if not database.create_content(content_name=form.content_name.data, browser=True, url=form.content_url.data):
            flash("Failed to add content. {} already exists.".format(form.content_name.data), "danger")
        return redirect(url_for("routes.content_home"))
    return render_template("add_browser_content.html", form=form)


@routes.route("/content/add_script_content",  methods=['GET', 'POST'])
def add_script_content():
    form = forms.ScriptContentForm(request.form)
    if request.method == 'POST' and form.validate():
        if not database.create_content(content_name=form.content_name.data, script=True, script_body=form.content_script.data):
            flash("Failed to add content. {} already exists.".format(form.content_name.data), "danger")
        return redirect(url_for("routes.content_home"))
    return render_template("add_script_content.html", form=form)


@routes.route("/clients/update_content_ajax", methods=['GET', 'POST'])
def client_update_content_ajax():
    content_id = request.form['content_id']
    client_id = request.form['client_id']
    database.update_client_content(client_id, content_id)
    print("{} - {}".format(content_id, client_id))
    return "a"
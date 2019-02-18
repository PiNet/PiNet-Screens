from flask import Blueprint, render_template, request, make_response, redirect, flash, url_for

import forms
import lts_conf

lts_conf_path = "test_data/lts.conf"

routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route("/clients",  methods=['GET', 'POST'])
@routes.route("/clients/edit/<client_mac>",  methods=['GET', 'POST'])
def clients_home(client_mac=None):
    form = forms.ClientForm(request.form)
    lts = lts_conf.LtsConf(lts_conf_path)
    clients = lts.raspberry_pis
    if request.method == 'POST' and form.validate():
        lts.add_update_client(mac_address=form.mac_address.data, location=form.location.data, hostname=form.hostname.data)
    if client_mac and request.method == "GET":
        client = lts.get_client(client_mac)
        form.mac_address.default = client.mac_address
        form.hostname.default = client.hostname
        form.location.default = client.location
        form.process()

    return render_template("clients_home.html", form=form, clients = clients)


@routes.route("/clients/disable_auto_login/<unique_id>")
def disable_auto_login(unique_id):
    lts = lts_conf.LtsConf(lts_conf_path)
    clients = lts.raspberry_pis
    for client in clients:
        if client.unique_id == unique_id:
            client.ldm_autologin = False
            lts.write_conf()
            return redirect(url_for("routes.clients_home"))


@routes.route("/clients/enable_auto_login/<unique_id>")
def enable_auto_login(unique_id):
    lts = lts_conf.LtsConf(lts_conf_path)
    clients = lts.raspberry_pis
    for client in clients:
        if client.unique_id == unique_id:
            client.ldm_autologin = True
            lts.write_conf()
            return redirect(url_for("routes.clients_home"))

@routes.route("/content")
def content_home():
    pass




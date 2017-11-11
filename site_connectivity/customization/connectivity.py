
from __future__ import unicode_literals
import frappe
from frappe import _,msgprint
from frappe.model.document import Document
import json
import subprocess
from subprocess import Popen,PIPE
import os
import hashlib
import re
import requests
import json


HEADERS = {"Content-Type": "application/json"}
@frappe.whitelist()
def api_site():
	"""Get API/REST Data with respective site"""
	from collections import defaultdict
	data = defaultdict(dict)
	sites = frappe.utils.get_sites()
	auth = {"usr": "info@indictranstech.com", "pwd": "indictrans" }
	headers = {}
	session_obj = requests.session()
	if os.path.exists('currentsite.txt'):
		with open('currentsite.txt') as f:
			currentsite = [f.read().strip()]
	try:
		for site in sites:
			if site not in currentsite:
				req = session_obj.post("http://"+site+"/api/method/login", auth = None, data = auth, headers = headers)
				user_req = session_obj.get("http://"+site+"/api/method/site_connectivity.customization.connectivity.process_singleton_site")
				req_close = session_obj.get("http://"+site+"/api/method/logout")
				api_data = user_req.json()
				data.update({site:api_data})
	except Exception, e:
		data.update({site:"Incomplete Setup"})
	process_data(data)

def process_data(data):
	final_dict = {}
	has_session_count = []

	for site,value in data.items():
		registered_user = frappe.get_doc("Site Configurations",site.split(".")[0].upper())
		if value != "Incomplete Setup":
			user_list = [{"first_name":user.get('first_name'),"name":user.get('name'),"last_login":user.get('last_login'),"has_session":user.get('has_session')} 
				if user.get('name')==registered_user.email_address else None for user in value.get('message').get('active_users')]
			api_user = [user for user in user_list if user is not None]
			if api_user:
				for i in api_user:
					i.update({"cust_count":value.get('message').get('customer')})
				final_dict.update({site:api_user})
	for site,value in final_dict.items():
		registered_user = frappe.get_doc("Site Configurations",site.split(".")[0].upper())
		registered_user.last_signup = value[0].get('last_login')
		registered_user.customer_count = value[0].get('cust_count')
		registered_user.api_user_email = value[0].get('name')
		registered_user.save()
		has_session_count.append(value[0].get('has_session'))

	conf_doc = frappe.get_doc("Multitenancy Settings")
	conf_doc.session_count = sum(has_session_count)
	conf_doc.save()

@frappe.whitelist()
def process_singleton_site():
	site_data = {}
	try:
		api_user = frappe.db.get_value("User",'info@indictranstech.com',"name")
		if api_user:
			active_users = frappe.db.sql("""select name,last_login,first_name ,last_name,(select count(*) from tabSessions where user=tabUser.name
	    						and timediff(now(), lastupdate) < time("01:00:00")) as has_session from tabUser
	    						where enabled=1 and last_login is not null and ifnull(user_type, '')!='Website User' and name not in ('Guest', 'Administrator','info@indictranstech.com')""",as_dict=1)
			customer = frappe.db.sql("""select count(name) as cust_count from `tabCustomer`""",as_dict=1)
			site_data.update({"active_users" : active_users,"customer":customer[0].get('cust_count')})
	except Exception, e:
		site_data.update({"resp":"error"})
		error_log = frappe.new_doc("Error Log")
		error_log.method = "Api Dashboard"
		error_log.error = e
		error_log.save()
	return site_data	


def after_install():
	from frappe.desk.page.setup_wizard.setup_wizard import add_all_roles_to
	user = frappe.new_doc("User")
	user.email = "info@indictranstech.com"
	user.first_name = "Indictranstech"
	user.send_welcome_email = 0
	user.new_password = "indictrans"
	user.save()
	add_all_roles_to(user.name)

def user_permission_query(user):
	return """(`tabUser`.name != 'info@indictranstech.com')"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "site_connectivity"
app_title = "Site Connectivity"
app_publisher = "Indictrans"
app_description = "Database Connection"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "chaitrali.w@indictranstech.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/site_connectivity/css/site_connectivity.css"
# app_include_js = "/assets/site_connectivity/js/site_connectivity.js"

# include js, css files in header of web template
# web_include_css = "/assets/site_connectivity/css/site_connectivity.css"
# web_include_js = "/assets/site_connectivity/js/site_connectivity.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "site_connectivity.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "site_connectivity.install.before_install"
after_install = "site_connectivity.customization.connectivity.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "site_connectivity.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"User": "site_connectivity.customization.connectivity.user_permission_query"
}
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"site_connectivity.tasks.all"
# 	],
# 	"daily": [
# 		"site_connectivity.tasks.daily"
# 	],
	"all": [
		"site_connectivity.customization.connectivity.api_site"
	]
# 	"weekly": [
# 		"site_connectivity.tasks.weekly"
# 	]
# 	"monthly": [
# 		"site_connectivity.tasks.monthly"
# 	]
}

# Testing
# -------

# before_tests = "site_connectivity.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "site_connectivity.event.get_events"
# }


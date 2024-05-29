# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['catalystwan',
 'catalystwan.api',
 'catalystwan.api.configuration_groups',
 'catalystwan.api.configuration_groups.parcels',
 'catalystwan.api.templates',
 'catalystwan.api.templates.device_template',
 'catalystwan.api.templates.models',
 'catalystwan.api.templates.payloads.aaa',
 'catalystwan.api.templates.payloads.cisco_vpn',
 'catalystwan.api.templates.payloads.tenant',
 'catalystwan.endpoints',
 'catalystwan.endpoints.configuration',
 'catalystwan.endpoints.configuration.device',
 'catalystwan.endpoints.configuration.feature_profile.sdwan',
 'catalystwan.endpoints.configuration.policy',
 'catalystwan.endpoints.configuration.policy.definition',
 'catalystwan.endpoints.configuration.policy.list',
 'catalystwan.endpoints.monitoring',
 'catalystwan.endpoints.real_time_monitoring',
 'catalystwan.endpoints.troubleshooting_tools',
 'catalystwan.integration_tests',
 'catalystwan.models',
 'catalystwan.models.configuration',
 'catalystwan.models.configuration.feature_profile',
 'catalystwan.models.configuration.feature_profile.sdwan.management',
 'catalystwan.models.configuration.feature_profile.sdwan.policy_object',
 'catalystwan.models.configuration.feature_profile.sdwan.policy_object.policy',
 'catalystwan.models.configuration.feature_profile.sdwan.policy_object.security',
 'catalystwan.models.configuration.feature_profile.sdwan.service',
 'catalystwan.models.configuration.feature_profile.sdwan.service.lan',
 'catalystwan.models.configuration.feature_profile.sdwan.system',
 'catalystwan.models.configuration.feature_profile.sdwan.transport',
 'catalystwan.models.misc',
 'catalystwan.models.monitoring',
 'catalystwan.models.policy',
 'catalystwan.models.policy.definitions',
 'catalystwan.tests',
 'catalystwan.tests.templates',
 'catalystwan.tests.templates.models',
 'catalystwan.utils',
 'catalystwan.utils.feature_template',
 'catalystwan.workflows']

package_data = \
{'': ['*'],
 'catalystwan.api.templates.payloads.aaa': ['feature/*'],
 'catalystwan.api.templates.payloads.cisco_vpn': ['feature/*'],
 'catalystwan.tests.templates': ['definitions/*',
                                 'definitions/basic/*',
                                 'schemas/*',
                                 'schemas/basic/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'attrs>=21.4.0,<22.0.0',
 'ciscoconfparse==1.9.41',
 'clint>=0.5.1,<0.6.0',
 'flake8-quotes>=3.3.1,<4.0.0',
 'packaging>=23.0,<24.0',
 'pydantic>=2.5,<3.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests-toolbelt>=1.0.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'tenacity>=8.1.0,<9.0.0',
 'typing-extensions>=4.6.1,<5.0.0']

setup_kwargs = {
    'name': 'catalystwan',
    'version': '0.33.8',
    'description': 'Cisco Catalyst WAN SDK for Python',
    'long_description': '<p align="center">\n  <a href="#"><img src="docs/images/catalystwan.svg" alt="Cisco Catalyst WAN SDK Logo" style="height:150px" />\n</p>\n\n[![Python-Supported](https://img.shields.io/static/v1?label=Python&logo=Python&color=3776AB&message=3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12)](https://www.python.org/)\n\nCisco Catalyst WAN SDK is a package for creating simple and parallel automatic requests via official SD-WAN Manager API. It is intended to serve as a multiple session handler (provider, provider as a tenant, tenant). The library is not dependent on environment which is being run in, you just need a connection to any SD-WAN Manager.\n\n## Important Notice: Early Beta Release\n\nWelcome to the Cisco Catalyst WAN SDK!\n\nWe are thrilled to announce that Cisco Catalyst WAN SDK is now available in early beta. This is an exciting step forward in enabling developers to harness the full potential of Cisco\'s networking solutions.  Please be aware that, as an early beta release, this version of the SDK is still undergoing development and testing. As such, it is provided "as is" and support to address any issues are limited and best effort.\n\n## Not recommend to use in production environments.\nWe encourage developers to explore and test the SDK\'s capabilities, but please exercise caution when using it in production environments.  We are dedicated to improving the Cisco Catalyst WAN SDK and we value your input. Your feedback is crucial to us-it will guide us in refining and enhancing the SDK to better meet your needs.\nTo report any issues, share your insights, or suggest improvements, please visit our Issues page on GitHub or reach out to us through the provided communication channels.\n\nThank you for being a part of our development journey!\n\n## Installation\n```console\npip install catalystwan\n```\n\n## Manager Session\nIn order to execute SDK APIs **ManagerSession** needs to be created. The fastest way to get started is to use `create_manager_session()` method which configures session, performs authentication for given credentials and returns **ManagerSession** instance in operational state. **ManagerSession** provides a collection of supported APIs in `api` instance variable.\nPlease check example below:\n\n```python\nfrom catalystwan.session import create_manager_session\n\nurl = "example.com"\nusername = "admin"\npassword = "password123"\n\nwith create_manager_session(url=url, username=username, password=password) as session:\n    devices = session.api.devices.get()\n    print(devices)\n```\n**ManagerSession** extends [requests.Session](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects) so all functionality from [requests](https://requests.readthedocs.io/en/latest/) library is avaiable to user, it also implements python [contextmanager](https://docs.python.org/3.8/library/contextlib.html#contextlib.contextmanager) and automatically frees server resources on exit.\n\n<details>\n    <summary> <b>Configure Manager Session before using</b> <i>(click to expand)</i></summary>\n\nIt is possible to configure **ManagerSession** prior sending any request.\n\n```python\nfrom catalystwan.session import ManagerSession\n\nurl = "example.com"\nusername = "admin"\npassword = "password123"\n\n# configure session using constructor - nothing will be sent to target server yet\nsession = ManagerSession(url=url, username=username, password=password)\n# login and send requests\nsession.login()\nsession.get("/dataservice/device")\nsession.close()\n```\nWhen interacting with the SDWAN Manager API without using a context manager, it\'s important \nto manually execute the `close()` method to release the user session resource.\nEnsure that the `close()` method is called after you have finished using the session to maintain optimal resource management and avoid potential errors.\n\n</details>\n\n<details>\n    <summary> <b>Login as Tenant</b> <i>(click to expand)</i></summary>\n\nTenant domain needs to be provided in url together with Tenant credentials.\n\n```python\nfrom catalystwan.session import create_manager_session\n\nurl = "tenant.example.com"\nusername = "tenant_user"\npassword = "password123"\n\nwith create_manager_session(url=url, username=username, password=password) as session:\n    print(session.session_type)\n```\n\n</details>\n\n<details>\n    <summary> <b>Login as Provider-as-Tenant</b> <i>(click to expand)</i></summary>\n\nTenant `subdomain` needs to be provided as additional argument together with Provider credentials.\n\n```python\nfrom catalystwan.session import create_manager_session\n\nurl = "example.com"\nusername = "provider"\npassword = "password123"\nsubdomain = "tenant.example.com"\n\nwith create_manager_session(url=url, username=username, password=password, subdomain=subdomain) as session:\n    print(session.session_type)\n```\n\n</details>\n\n\n\n## API usage examples\nAll examples below assumes `session` variable contains logged-in [Manager Session](#Manager-Session) instance.\n\n<details>\n    <summary> <b>Get devices</b> <i>(click to expand)</i></summary>\n\n```python\ndevices = session.api.devices.get()\n```\n\n</details>\n\n<details>\n    <summary> <b>Admin Tech</b> <i>(click to expand)</i></summary>\n\n```Python\nadmin_tech_file = session.api.admin_tech.generate("172.16.255.11")\nsession.api.admin_tech.download(admin_tech_file)\nsession.api.admin_tech.delete(admin_tech_file)\n```\n</details>\n\n<details>\n    <summary> <b>Speed test</b> <i>(click to expand)</i></summary>\n\n```python\ndevices = session.api.devices.get()\nspeedtest = session.api.speedtest.speedtest(devices[0], devices[1])\n```\n\n</details>\n\n<details>\n    <summary> <b>Upgrade device</b> <i>(click to expand)</i></summary>\n\n```python\n# Prepare devices list\ncontrollers = session.endpoints.configuration_device_inventory.get_device_details(\'controllers\')\nvsmarts = controllers.filter(personality=Personality.VSMART)\nimage = "viptela-20.7.2-x86_64.tar.gz"\n\n# Upload image\nsession.api.repository.upload_image(image)\n\n# Install software\n\ninstall_task = session.api.software.install(devices=vsmarts, image=image)\n\n# Check action status\ninstall_task.wait_for_completed()\n```\n\n</details>\n\n<details>\n    <summary> <b>Get alarms</b> <i>(click to expand)</i></summary>\nTo get all alarms:\n\n```python\nalarms = session.api.alarms.get()\n```\n\nTo get all not viewed alarms:\n\n```python\nnot_viewed_alarms = session.api.alarms.get().filter(viewed=False)\n```\n\nTo get all alarms from past `n` hours:\n\n```python\nn = 24\nalarms_from_n_hours = session.api.alarms.get(from_time=n)\n```\n\nTo get all critical alarms from past `n` hours:\n\n```python\nfrom catalystwan.utils.alarm_status import Severity\nn = 48\ncritical_alarms = session.api.alarms.get(from_time=n).filter(severity=Severity.CRITICAL)\n```\n\n</details>\n\n<details>\n    <summary> <b>Users</b> <i>(click to expand)</i></summary>\n\n```python\n# Get all users\nsession.api.users.get()\n\n# Create user\nfrom catalystwan.endpoints.administration_user_and_group import User\nnew_user = User(username="new_user", password="new_user", group=["netadmin"], description="new user")\nsession.api.users.create(new_user)\n\n# Update user data\nnew_user_update = UserUpdateRequest(username="new_user", group=["netadmin", "netops"], locale="en_US", description="updated-new_user-description")\nsession.api.users.update(new_user_update)\n\n# Update user password\nsession.api.users.update_password("new_user", "n3W-P4s$w0rd")\n\n# Reset user\nsession.api.users.reset("new_user")\n\n# Delete user\nsession.api.users.delete("new_user")\n\n# Get current user authentication type and role\nsession.api.users.get_auth_type()\nsession.api.users.get_role()\n```\n\n</details>\n\n<details>\n    <summary> <b>User Groups</b> <i>(click to expand)</i></summary>\n\n```python\n# Get all user groups\nsession.api.user_groups.get()\n\n# Create user group\ngroup = UserGroup("new_user_group", [])\ngroup.enable_read({"Audit Log", "Alarms"})\ngroup.enable_read_and_write({"Device Inventory"})\nsession.api.user_groups.create(group)\n\n# Update user group\ngroup.disable({"Alarms"})\nsession.api.user_groups.update(group)\n\n# Delete user group\nsession.api.user_groups.delete(group.group_name)\n```\n\n</details>\n\n</details>\n\n<details>\n    <summary> <b>Sessions</b> <i>(click to expand)</i></summary>\n\n```python\n# Get all active sessions\nactive_sessions = session.api.sessions.get()\n\n# Invalidate sessions for given user\nnew_user_sessions = active_sessions.filter(raw_username="new_user")\nsession.api.sessions.invalidate(new_user_sessions)\n```\n\n</details>\n\n<details>\n    <summary> <b>Resource Groups</b> <i>(click to expand)</i></summary>\n\n```python\n# get resource groups\nsession.api.resource_groups.get()\n\n# create resource group\nnew_resource_group = ResourceGroup(\n    name="new_resource_group",\n    desc="Custom Resource Group #1",\n    siteIds=[]\n)\nsession.api.resource_groups.create(new_resource_group)\n\n# update resource group\nresource_group = session.api.resource_groups.get().filter(name="new_resource_group").single_or_default()\nupdated_resource_group = ResourceGroupUpdateRequest(\n    id=resource_group.id,\n    name=resource_group.name,\n    desc="Custom Resource Group #1 with updated description and site ids",\n    siteIds=[200]\n)\n\n# switch to resource group view\nsession.api.resource_groups.switch("new_resource_group")\n\n# delete resource group\nsession.api.resource_groups.delete(resource_group.id)\n```\n\n</details>\n\n<details>\n    <summary> <b>Tenant management</b> <i>(click to expand)</i></summary>\n\n```python\napi = session.api.tenant_management\n# create tenants\ntenants = [\n    Tenant(\n        name="tenant1",\n        org_name="CiscoDevNet",\n        subdomain="alpha.bravo.net",\n        desc="This is tenant for unit tests",\n        edge_connector_enable=True,\n        edge_connector_system_ip="172.16.255.81",\n        edge_connector_tunnel_interface_name="GigabitEthernet1",\n        wan_edge_forecast=1,\n    )\n]\ncreate_task = api.create(tenants)\ncreate_task.wait_for_completed()\n# list all tenants\ntenants_data = api.get_all()\n# pick tenant from list by name\ntenant = tenants_data.filter(name="tenant1").single_or_default()\n# get selected tenant id\ntenant_id = tenant.tenant_id\n# get vsession id of selected tenant\nvsessionid = api.vsession_id(tenant_id)\n# delete tenant by ids\ndelete_task = api.delete([tenant_id])\ndelete_task.wait_for_completed()\n# others\napi.get_hosting_capacity_on_vsmarts()\napi.get_statuses()\napi.get_vsmart_mapping()\n```\n</details>\n\n<details>\n    <summary> <b>Tenant migration</b> <i>(click to expand)</i></summary>\n\n```python\nfrom pathlib import Path\nfrom catalystwan.session import create_manager_session\nfrom catalystwan.models.tenant import TenantExport\nfrom catalystwan.workflows.tenant_migration import migration_workflow\n\ntenant = TenantExport(\n    name="mango",\n    desc="Mango tenant description",\n    org_name="Provider Org-Mango Inc",\n    subdomain="mango.fruits.com",\n    wan_edge_forecast=100,\n    migration_key="MangoTenantMigrationKey",   # only for SDWAN Manager >= 20.13\n    is_destination_overlay_mt=True,            # only for SDWAN Manager >= 20.13\n)\n\nwith create_manager_session(url="10.0.1.15", username="st-admin", password="") as origin_session, \\\n     create_manager_session(url="10.9.0.16", username="mt-provider-admin", password="") as target_session:\n    migration_workflow(\n        origin_session=origin_session,\n        target_session=target_session,\n        workdir=Path("workdir"),\n        tenant=tenant,\n        validator="10.9.12.26"\n    )\n```\n\n`migration_workflow` performs multi-step migration procedure according to [Migrate Single-Tenant Cisco SD-WAN Overlay to Multitenant Cisco SD-WAN Deployment](https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/system-interface/vedge-20-x/systems-interfaces-book/sdwan-multitenancy.html#concept_sjj_jmm_z4b)\n\n\nSince 20.13 also MT to ST is supported (just provide suitable origin/target sessions, and `is_destination_overlay_mt` parameter)\n\n\nEach step of the `migration_workflow` procedure can be executed independently using api methods: `export_tenant`, `download`, `import_tenant`, `store_token`, `migrate_network`\n\n```python\norigin_api = origin_session.api.tenant_migration_api\ntarget_api = target_session.api.tenant_migration_api\ntenant_file = Path("~/tenant.tar.gz")\ntoken_file = Path("~/tenant-token.txt")\n# export\nexport_task = origin_api.export_tenant(tenant=tenant)\nremote_filename = export_task.wait_for_file()\n# download\norigin_api.download(export_path, remote_filename)\n# import\nimport_task = target_api.import_tenant(export_path, tenant.migration_key)\nimport_task.wait_for_completed()\n# get token\nmigration_id = import_task.import_info.migration_token_query_params.migration_id\ntarget_api.store_token(migration_id, token_path)\n# migrate network\nmigrate_task = origin_api.migrate_network(token_path)\nmigrate_task.wait_for_completed()\n```\n</details>\n\n### Note:\nTo remove `InsecureRequestWarning`, you can include in your scripts (warning is suppressed when `catalystwan_devel` environment variable is set):\n```Python\nimport urllib3\nurllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)\n```\n\n## Catching Exceptions\n```python\ntry:\n    session.api.users.delete("bogus-user-name")\nexcept ManagerHTTPError as error:\n    # Process an error.\n    print(error.response.status_code)\n    print(error.info.code)\n    print(error.info.message)\n    print(error.info.details)\n\n```\n\n## [Supported API endpoints](https://github.com/cisco-open/cisco-catalyst-wan-sdk/blob/main/ENDPOINTS.md)\n\n\n## [Contributing, bug reporting and feature requests](https://github.com/cisco-open/cisco-catalyst-wan-sdk/blob/main/CONTRIBUTING.md)\n\n## Seeking support\n\nYou can contact us by submitting [issues](https://github.com/cisco-open/cisco-catalyst-wan-sdk/issues), or directly via mail on catalystwan@cisco.com.\n',
    'author': 'kagorski',
    'author_email': 'kagorski@cisco.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cisco-open/cisco-catalyst-wan-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)

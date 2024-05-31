import click
import time
import arrow
from .api_wrapper import tenb_connection, navi_version, request_data
from .database import new_db_connection, db_query
import textwrap
from .sla import print_sla

tio = tenb_connection()


def get_licensed():
    data = request_data('GET', '/workbenches/asset-stats?date_range=90&filter.0.filter=is_licensed&filter.0.quality=eq&filter.0.value=true')
    number_of_assets = data['scanned']
    return number_of_assets


def get_scanners():
    try:
        click.echo("\n{:35s} {:20} {}".format("Scanner Name", "Scanner ID", "Scanner UUID"))
        click.echo("-" * 150)
        for nessus in tio.scanners.list():
            click.echo("{:35s} {:20} {}".format(str(nessus["name"]), str(nessus["id"]), str(nessus['uuid'])))
        click.echo()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


def compare_dates(given_date):
    today = arrow.now()
    try:
        given_date = arrow.get(given_date)
        days_difference = (today - given_date).days

        if days_difference > 35:
            return "no"
        else:
            return "yes"
    except ValueError:
        print("Invalid date format")


@click.group(help="Display information found in Tenable.io")
def display():
    pass


@display.command(help="Display all of the scanners")
def scanners():
    get_scanners()


@display.command(help="Display  all of the Users")
def users():
    try:
        click.echo("\n{:34s} {:40s} {:40s} {:10s} {}".format("User Name", "Login Email", "UUID", "ID", "Enabled"))
        click.echo("-" * 150)
        for user in tio.users.list():
            click.echo("{:34s} {:40s} {:40s} {:10s} {}".format(str(user["user_name"]), str(user["username"]), str(user['uuid']), str(user['id']), str(user['enabled'])))
        click.echo()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display all Exclusions")
def exclusions():
    try:
        for exclusion in tio.exclusions.list():
            click.echo("\n{} {}".format("Exclusion Name :", exclusion["name"]))
            click.echo("-" * 150)
            click.echo("{}".format(str(exclusion["members"])))
        click.echo()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display The actor and the action in the log file")
def logs():
    try:
        events = tio.audit_log.events()
        click.echo("{:24s} {:30s} {}".format("Event Date", "Action Taken", "User"))
        click.echo("-" * 150)

        for log in events:
            click.echo("{:24s} {:30s} {:30s}".format(str(log['received']), str(log['action']),
                                                     str(log['actor']['name'])))

        click.echo()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display running Scans")
def running():
    try:
        click.echo("\n{:60s} {:10s} {:30s}".format("Scan Name", "Scan ID", "Status"))
        click.echo("-" * 150)

        for scan in tio.scans.list():
            if scan['status'] == "running":
                click.echo("{:60s} {:10s} {:30s}".format(str(scan['name']), str(scan['id']), str(scan['status'])))

        click.echo()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display Scans")
@click.option("-a", is_flag=True, help="Display all scans")
def scans(a):
    try:
        click.echo("\n{:80s} {:5s} {:10s} {:40}".format("Scan Name", "ID", "Status", "UUID"))
        click.echo("-" * 150)

        if a:
            for scan in tio.scans.list():
                    try:
                        click.echo("{:80s} {:5s} {:10s} {:40}".format(textwrap.shorten(str(scan['name']), width=80), str(scan['id']), str(scan['status']),
                                                                    str(scan['uuid'])))
                    except KeyError:
                        click.echo("{:80s} {:5s} {:10s} {:40}".format(textwrap.shorten(str(scan['name']), width=80), str(scan['id']), str(scan['status']),
                                                                    "No UUID"))
        else:
            for scan in tio.scans.list():
                if str(compare_dates(scan['last_modification_date'])) == 'yes':
                    try:
                        click.echo("{:80s} {:5s} {:10s} {:40}".format(textwrap.shorten(str(scan['name']), width=80), str(scan['id']), str(scan['status']),
                                                                    str(scan['uuid'])))
                    except KeyError:
                        click.echo("{:80s} {:5s} {:10s} {:40}".format(textwrap.shorten(str(scan['name']), width=80), str(scan['id']), str(scan['status']),
                                                                    "No UUID"))
                else:
                    pass
        click.echo()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display NNM assets and their vulnerability scores")
def nnm():
    click.echo("\nChecking all NNM scanners for assets recently found...")
    click.echo("\n{:20} {:10} {}".format("IP Address", "Score", "Scan ID"))
    click.echo("-" * 150)

    for scan in tio.scans.list():
        try:
            if str(scan["type"]) == "pvs":
                resp = tio.get('scans/{}'.format(scan["id"]))
                data = resp.json()

                for host in data["hosts"]:
                    click.echo("{:20} {:10} {}".format(str(host["hostname"]), str(host["score"]), str(scan["id"])))

        except AttributeError:
            click.echo("\nCheck your permissions or your API keys\n")

        except KeyError:
            pass


@display.command(help="Display All Assets found in the last 30 days")
@click.option("--tag", default='', help="Display Assets membership of a given Tag.  "
                                        "Use Tag Value UUID found in the command 'navi display tags'")
def assets(tag):
    if tag:
        data = db_query("select ip_address, fqdn, aes, acr from assets LEFT JOIN tags ON uuid == asset_uuid where tag_uuid=='{}';".format(tag))

        click.echo("\nBelow are the assets that are apart of the Tag")
        click.echo("\n{:16} {:80} {:6} {}".format("IP Address", "FQDN", "AES", "ACR"))
        click.echo("-" * 150)
        try:
            for asset in data:
                ipv4 = str(asset[0])
                fqdn = str(asset[1])
                exposure_score = str(asset[2])
                acr = str(asset[3])

                click.echo("{:16} {:80} {:6} {}".format(ipv4, textwrap.shorten(fqdn, width=80), exposure_score, acr))
            click.echo()
        except TypeError:
            click.echo("\nThe Tag has no assets or the tag hasn't finished being processed by T.io\n")
    else:
        try:
            click.echo("\nBelow are the assets found in the last 30 days")
            click.echo("\n{:16} {:80} {:40} {:6}".format("IP Address", "FQDN", "UUID", "AES"))
            click.echo("-" * 150)
            asset_data = db_query("select ip_address, fqdn, uuid, aes from assets;")
            for asset in asset_data:

                click.echo("{:16} {:80} {:40} {:6} ".format(asset[0], textwrap.shorten(asset[1], width=80), asset[2], str(asset[3])))

            click.echo("\nTotal: {}\n\n".format(len(asset_data)))
        except AttributeError:
            click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display Scan Policies")
def policies():
    try:
        click.echo("\n{:40s} {:51s} {:10} {}".format("Policy Name", "Description", "ID", "Template ID"))
        click.echo("-" * 150)

        for policy in tio.policies.list():
            click.echo("{:40s} {:51s} {:10} {}".format(str(policy['name']), str(policy['description']), str(policy['id']),
                                                       policy['template_uuid']))
        click.echo()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display Cloud Connector Details and Status")
def connectors():
    try:
        resp = tio.get('settings/connectors')
        data = resp.json()

        click.echo("\n{:11s} {:40s} {:40s} {:30s} {}".format("Type", "Connector Name", "Connector ID", "Last Sync", "Schedule"))
        click.echo("-" * 150)
        schedule = "None"
        for conn in data["connectors"]:
            try:
                schedule = str(conn['schedule']['value']) + " " + str(conn['schedule']['units'])


                last_sync = conn['last_sync_time']
            except KeyError:
                last_sync = "Hasn't synced"

            click.echo("{:11s} {:40s} {:40s} {:30s} {}".format(str(conn['type']), str(conn['name']), str(conn['id']),
                                                               last_sync, schedule))
        click.echo()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display T.io Status and Account info")
def status():
    try:
        data = tio.server.properties()
        session_data = tio.session.details()
        click.echo("\nTenable IO Information")
        click.echo("-" * 25)
        click.echo("{} {}".format("Container ID : ", session_data["container_id"]))
        click.echo("{} {}".format("Container UUID :", session_data["container_uuid"]))
        click.echo("{} {}".format("Container Name : ", session_data["container_name"]))
        click.echo("{} {}".format("Site ID :", data["analytics"]["site_id"]))
        click.echo("{} {}".format("Region : ", data["region"]))

        click.echo("\nLicense information")
        click.echo("-" * 25)
        click.echo("{} {}".format("Licensed Assets : ", get_licensed()))
        click.echo("{} {}".format("Agents Used : ", data['license']["agents"]))
        try:
            click.echo("{} {}".format("Expiration Date : ", data['license']["expiration_date"]))
        except KeyError:
            pass
        click.echo("{} {}".format("Scanners Used : ", data['license']["scanners"]))
        click.echo("{} {}".format("Users : ", data["license"]["users"]))

        click.echo("\nEnabled Apps")
        click.echo("-" * 15)
        click.echo()
        try:
            for key in data["license"]["apps"]:
                click.echo(key)
                click.echo("-" * 5)
                try:
                    click.echo("{} {}".format("Expiration: ", str(data["license"]["apps"][key]["expiration_date"])))
                except KeyError:
                    pass
                click.echo("{} {}".format("Mode: ", str(data["license"]["apps"][key]["mode"])))
                click.echo()
        except KeyError:
            pass

    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display Agent information - Limit 5000 agents")
@click.option("-uuid", is_flag=True, help="Display Agent information including Agent UUID")
def agents(uuid):
    try:
        if uuid:
            click.echo("\n{:30s} {:20} {:20} {:20} {:6} {}".format("Agent Name", "IP Address", "Last Connect Time", "Last Scanned Time", "Status", "UUID"))
            click.echo("-" * 150)
        else:
            click.echo("\n{:30s} {:20} {:20} {:20} {:6} {}".format("Agent Name", "IP Address", "Last Connect Time", "Last Scanned Time", "Status", "Group(id)s"))
            click.echo("-" * 150)

        for agent in tio.agents.list():
            try:
                last_connect = agent['last_connect']
                last_connect_time = time.strftime("%b %d %H:%M:%S", time.localtime(last_connect))
            except KeyError:
                last_connect_time = "Unknown"

            try:
                last_scanned = agent['last_scanned']
                last_scanned_time = time.strftime("%b %d %H:%M:%S", time.localtime(last_scanned))
            except KeyError:
                # I assume if we can't pull as scanned time, it doesn't exist
                last_scanned_time = "Not Scanned"
            groups = ''
            try:
                for group in agent['groups']:
                    groups = groups + ", {}({})".format(group['name'], group['id'])
            except KeyError:
                pass

            try:
                agent_uuid = agent['uuid']
            except KeyError:
                agent_uuid = "unknown"

            if uuid:
                click.echo("{:30s} {:20s} {:20s} {:20s} {:6s} {}".format(textwrap.shorten(str(agent['name']), width=30),
                                                                         str(agent['ip']), str(last_connect_time),
                                                                         str(last_scanned_time), str(agent['status']),
                                                                         textwrap.shorten(agent_uuid, width=60)))
            else:
                click.echo("{:30s} {:20s} {:20s} {:20s} {:6s} {}".format(textwrap.shorten(str(agent['name']), width=30),
                                                                         str(agent['ip']), str(last_connect_time),
                                                                         str(last_scanned_time), str(agent['status']),
                                                                         textwrap.shorten(groups[1:], width=60)))
        click.echo()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display Target Groups")
def tgroups():
    try:
        print("\nTarget Group Name".ljust(41), "TG ID".ljust(10), "Owner".ljust(30), "Members")
        print("-" * 100)
        for targets in tio.target_groups.list():
            mem = targets['members']
            print(str(targets['name']).ljust(40), str(targets['id']).ljust(10), str(targets['owner']).ljust(30), textwrap.shorten(mem, width=60))
        print()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display Licensed Assets")
def licensed():
    try:
        click.echo("\n{} {}".format("Licensed Count: ", get_licensed()))
        click.echo()
        database = r"navi.db"
        conn = new_db_connection(database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT uuid, fqdn, last_licensed_scan_date from assets where last_licensed_scan_date !=' ';")
            data = cur.fetchall()

            click.echo("{:40s} {:65s} {}".format("Asset UUID", "Full Qualified Domain Name", "Licensed Date"))
            click.echo("-" * 150)
            click.echo()
            count = 0
            for asset in data:
                count += 1
                uuid = asset[0]
                fqdn = asset[1]
                licensed_date = asset[2]
                click.echo("{:40s} {:65s} {}".format(str(uuid), str(fqdn), licensed_date))
        click.echo("\nTotal: {}".format(count))
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display Tags Information")
def tags():
    try:
        click.echo("\n{:55s} {:55s} {}".format("Category", "  Value", "  Value UUID"))
        click.echo("-" * 150)
        for tag_values in tio.tags.list():
            try:
                tag_value = tag_values['value']
                uuid = tag_values['uuid']
            except KeyError:
                tag_value = "Value Not Set Yet"
                uuid = "NO Value set"
            click.echo("{:55s} : {:55s} {}".format(textwrap.shorten(str(tag_values['category_name']), width=55),
                                                   textwrap.shorten(str(tag_value), width=55),
                                                   str(uuid)))
        click.echo()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display Tag Categories and UUIDs")
def categories():
    try:
        click.echo("\n{:31s} {}".format("Tag Categories", "Category UUID"))
        click.echo("-" * 150)
        for cats in tio.tags.list_categories():
            category_name = cats['name']
            category_uuid = cats['uuid']
            click.echo("{:31s} {}".format(str(category_name), str(category_uuid)))
        click.echo()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display Network Information including scanner counts")
def networks():
    try:
        click.echo("\n{:45s} {:16} {}".format("Network Name", "# of Scanners", "UUID"))
        click.echo("-" * 150)

        for network in tio.networks.list():
            click.echo("{:45s} {:16} {}".format(str(network['name']), str(network['scanner_count']),
                                                str(network['uuid'])))
        click.echo()

    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display the current Navi Version")
def version():
    click.echo("\nCurrent Navi Version: {}\n".format(navi_version()))


@display.command(help="Display User group information")
@click.option('--membership', required=True, default='', help="Display Users that apart of a particular user group using the user group ID")
def usergroups(membership):
    try:
        if membership:
            click.echo("\n{:35s} {:40s} {:40s} {:10} {}".format("User Name", "Login email", "User UUID", "User ID",
                                                                "Enabled?"))
            click.echo("-" * 150)
            for user in tio.groups.list_users(membership):
                click.echo("{:35s} {:40s} {:40s} {:10} {}".format(str(user["name"]), str(user["username"]),
                                                                  str(user['uuid']), str(user['id']),
                                                                  str(user["enabled"])))
            click.echo()
        else:
            click.echo("\n{:35s} {:10s} {:40s} {}".format("Group Name", "Group ID", "Group UUID", "User Count"))
            click.echo("-" * 150)

            for user_group in tio.groups.list():
                click.echo("{:35s} {:10s} {:40s} {}".format(str(user_group['name']), str(user_group['id']),
                                                            str(user_group['uuid']), str(user_group['user_count'])))
            click.echo()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display All Credentials, including Type and Credential UUID")
def credentials():
    try:

        click.echo("\n{:25s} {:25s} {:25s} {:25s} {:40s}".format("Credential Name", "Created By",
                                                                 "Credential Type", "Category", "Credential UUID"))
        click.echo("-" * 150)

        for cred in tio.credentials.list():
            creator = cred['created_by']['display_name']
            name = cred['name']
            cred_type = cred['type']['name']
            cred_uuid = cred['uuid']
            category = cred['category']['name']
            click.echo("{:25s} {:25s} {:25s} {:25s} {:40s}".format(textwrap.shorten(name, width=25),
                                                                   textwrap.shorten(creator, width=25),
                                                                   textwrap.shorten(cred_type, width=25),
                                                                   textwrap.shorten(category, width=25),
                                                                   textwrap.shorten(cred_uuid, width=40)))
        click.echo()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display Asset and Vulnerability Export Job information")
@click.option('-a', help="Display Asset Export Jobs", is_flag=True)
@click.option('-v', help="Display Vulnerability Export Jobs", is_flag=True)
def exports(a, v):
    if not a and not v:
        click.echo("\nYou need to use '-a' or '-v' to select your export type. (assets vs vulns)\n")

    current_time = time.time()
    time_frame = (current_time - (86400 * 3)) * 1000
    if a:
        export_data = request_data('GET', '/assets/export/status')
        click.echo("{:45s} {:20s} {:10s} {:45s} {:10s} {}".format("\nAsset Export UUID", "Created Date", "Status",
                                                                  "Export Filter Used",  "Chunk Size", "Total Chunks"))
        click.echo('-' * 150)

        for export in export_data['exports']:
            compare_time = export['created']
            newtime = arrow.Arrow.fromtimestamp(compare_time)

            if compare_time > time_frame:
                export_uuid = export['uuid']
                export_status = export['status']
                export_chunk_size = export['num_assets_per_chunk']
                export_filter = export['filters']
                export_total_chunks = export['total_chunks']

                click.echo("{:44s} {:20s} {:10s} {:45s} {:10d} {}".format(export_uuid, newtime.format('MM-DD-YYYY'),
                                                                          export_status, export_filter,
                                                                          export_chunk_size, export_total_chunks))

    if v:
        vuln_export_data = request_data('GET', '/vulns/export/status')
        click.echo("{:45s} {:20s} {:10s} {:45s} {:10s} {}".format("\nVulnerability Export UUID", "Created Date",
                                                                  "Status", "States", "Chunk Size", "Total Chunks"))
        click.echo('-' * 150)

        for vuln_export in vuln_export_data['exports']:
            vuln_compare_time = vuln_export['created']
            vuln_newtime = arrow.Arrow.fromtimestamp(vuln_compare_time)

            if vuln_compare_time > time_frame:
                export_uuid = vuln_export['uuid']
                export_status = vuln_export['status']
                export_chunk_size = vuln_export['num_assets_per_chunk']
                export_filter = str(vuln_export['filters']['state'])
                vuln_export_total_chunks = vuln_export['total_chunks']

                click.echo("{:44s} {:20s} {:10s} {:45s} {:10d} {}".format(export_uuid, vuln_newtime.format('MM-DD-YYYY'),
                                                                          export_status, export_filter,
                                                                          export_chunk_size, vuln_export_total_chunks))

    click.echo()


@display.command(help="Display Authorization information for a user given a User ID")
@click.argument('uid')
def auth(uid):
    info = request_data("GET", "/users/{}/authorizations".format(uid))

    click.echo("\n{:45} {:20} {:20} {:20} {}".format("Account_UUID", "API Permitted", "Password Permitted",
                                                     "SAML Permitted", "User_UUID"))
    click.echo("-" * 150)

    click.echo("{:45} {:20} {:20} {:20} {}".format(str(info['account_uuid']), str(info['api_permitted']),
                                                   str(info['password_permitted']), str(info['saml_permitted']),
                                                   str(info['user_uuid'])))

    click.echo()


@display.command(help="Display Scan Policy Templates")
@click.option("-policy", is_flag=True, help="Display all Policy Templates")
@click.option("-scan", is_flag=True, help="Display all Scan Templates")
def templates(policy, scan):
    template_type = ""

    if policy:
        template_type = "policy"
    if scan:
        template_type = "scan"

    if template_type:
        try:
            click.echo("\n{:40s} {:61s} {}".format("Policy Name", "Description", "Template ID"))
            click.echo("-" * 150)

            for policy in tio.editor.template_list(str(template_type)):
                click.echo("{:40s} {:61s} {}".format(str(policy['name']), str(policy['title']),
                                                     policy['uuid']))
            click.echo()
        except AttributeError:
            click.echo("\nCheck your permissions or your API keys\n")
    else:
        click.echo("\nYou must use '-scan' or '-policy'")


@display.command(help="Display completed Audit files and Audit information")
@click.option('--name', default=None, help="Display all of the Assets with completed Audits for the Given Audit name")
@click.option('--uuid', default=None, help="Display all compliance findings for a given Asset UUID")
def audits(name, uuid):

    if name and uuid:
        data = db_query("SELECT asset_uuid, check_name, status FROM compliance where audit_file='{}' "
                        "and asset_uuid='{}';".format(name, uuid))

        click.echo("{:45} {:85} {}".format("\nAsset UUID", " Check Name", " Status"))
        click.echo("-" * 150)
        click.echo()
        for finding in data:
            click.echo("{:45} {:85} {}".format(textwrap.shorten(str(finding[0]), width=45),
                                               textwrap.shorten(str(finding[1]), width=85),
                                               finding[2]))
        click.echo()

    elif name:
        data = db_query("SELECT asset_uuid, check_name, status FROM compliance where audit_file='{}';".format(name))

        click.echo("{:45} {:85} {}".format("\nAsset UUID", " Check Name", " Status"))
        click.echo("-" * 150)
        click.echo()
        for finding in data:
            click.echo("{:45} {:85} {}".format(textwrap.shorten(str(finding[0]), width=45),
                                               textwrap.shorten(str(finding[1]), width=85),
                                               finding[2]))
        click.echo()

    elif uuid:
        data = db_query("SELECT asset_uuid, check_name, status FROM compliance where asset_uuid='{}';".format(uuid))

        click.echo("{:45} {:85} {}".format("\nAsset UUID", " Check Name", " Status"))
        click.echo("-" * 150)
        click.echo()
        for finding in data:
            click.echo("{:45} {:85} {}".format(textwrap.shorten(str(finding[0]), width=45),
                                               textwrap.shorten(str(finding[1]), width=85),
                                               finding[2]))
        click.echo()

    else:
        compliance_data = db_query("SELECT audit_file from compliance;")
        compliance_list = []

        for audit in compliance_data:
            if audit not in compliance_list:
                compliance_list.append(audit)

        click.echo("\nCompleted Audits")
        click.echo("-" * 80)
        click.echo()

        for name in compliance_list:
            click.echo(name[0])

        click.echo()


@display.command(help="Display Permissions")
def permissions():
    permission_data = request_data("GET", "/api/v3/access-control/permissions")
    try:
        click.echo("\n{:80s} {}".format("Name - Tag Category:Value - [perms]", "Subject(s)"))
        click.echo("-" * 150)

        for perm in permission_data['permissions']:
            subject_names = []
            for names in perm['subjects']:
                try:
                    subject_names.append(names['name'])
                except KeyError:
                    # All admins perm has no name
                    pass
            click.echo("{:80s} {}".format(textwrap.shorten(perm['name'], width=80),
                                          textwrap.shorten("{}".format(subject_names), width=70)))
        click.echo()
    except AttributeError:
        click.echo("\nCheck your permissions or your API keys\n")


@display.command(help="Display custom attributes")
def attributes():
    custom_attributes = request_data("GET", "/api/v3/assets/attributes")

    click.echo("\n{:60s} {:50} {}".format("Attribute Name", "Description", "UUID"))
    click.echo("-" * 150)
    for attr in custom_attributes['attributes']:
        attr_name = attr['name']
        attr_description = attr['description']
        attr_uuid = attr['id']
        click.echo("{:60s} {:50} {}".format(attr_name, attr_description, attr_uuid))
    click.echo()


@display.command(help="Display curent SLA")
def sla():
    print_sla()

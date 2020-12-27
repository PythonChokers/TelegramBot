import telebotdb


list_services_sumcash = telebotdb.get_impact_by_service()
list_masters_sumcash = telebotdb.get_impact_by_master()


services = {}
for service in telebotdb.get_service():
    services[service.id] = str(service.name)


masters = {}
for master in telebotdb.get_master():
    masters[master.id] = str(master.name)

def sumcash():
    send_sumcash = 0
    for srcash in list_services_sumcash:
        send_sumcash += int(srcash.sum)
    return send_sumcash

def services_impact():
    send_services = {}
    for srcash in list_services_sumcash:
        send_services[services[srcash.id]] = str(srcash.sum)
    return send_services


def masters_impact():
    send_masters = {}
    for mscash in list_masters_sumcash:
        send_masters[masters[mscash.id]] = str(mscash.sum)
    return send_masters

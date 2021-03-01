import base64

from kapitan.inputs.kadet import BaseObj, inventory, CompileError

inv = inventory()

class Machine(BaseObj):
    def new(self):
        self.need("name")
        self.need("subtype")
        self.update_root("lib/machine.yaml")

    def body(self):
        self.root.metadata.name = self.kwargs.name
        self.root.metadata.namespace = inv.parameters.cluster.namespace
        self.root.metadata.labels['kaas.mirantis.com/region'] = inv.parameters.cluster.region
        self.root.metadata.labels['kaas.mirantis.com/provider'] = inv.parameters.cluster.provider
        self.root.metadata.labels['cluster.sigs.k8s.io/cluster-name'] = inv.parameters.cluster.name
        if self.kwargs.subtype is 'managers':
            self.root.spec.providerSpec.value.hostSelector.matchLabels['hostlabel.bm.kaas.mirantis.com/controlplane'] = 'true'
        elif self.kwargs.subtype is 'workers_storage':
            self.root.spec.providerSpec.value.hostSelector.matchLabels['hostlabel.bm.kaas.mirantis.com/storage'] = 'true'
        else:
            self.root.spec.providerSpec.value.hostSelector.matchLabels['hostlabel.bm.kaas.mirantis.com/worker'] = 'true'
        self.root.spec.providerSpec.value.hostSelector.matchLabels.baremetal = "hw-" + self.kwargs.name + "-" + self.kwargs.subtype
        if 'BMHProfile' in inv.parameters.hosts[self.kwargs.subtype]:
            self.root.spec.providerSpec.value.bareMetalHostProfile.name = inv.parameters.hosts[self.kwargs.subtype].BMHProfile.name 
            self.root.spec.providerSpec.value.bareMetalHostProfile.namespace = inv.parameters.hosts[self.kwargs.subtype].BMHProfile.namespace
        if 'l2template' in inv.parameters.hosts[self.kwargs.subtype]:
            self.root.spec.providerSpec.value.l2TemplateSelector.name = inv.parameters.hosts[self.kwargs.subtype].l2template.name
        if 'nodeLabels' in inv.parameters.hosts[self.kwargs.subtype]:
            for key, value in inv.parameters.hosts[self.kwargs.subtype].nodeLabels.items(): 
                self.root.spec.providerSpec.value.nodeLabels.key = value
        if 'tf_ctl' in inv.parameters.hosts:
            tf = True
        else:
            tf = False
        if self.kwargs.subtype == 'workers_osctl':
            self.root.spec.providerSpec.value.nodeLabels = [{'key': 'openstack-control-plane', 'value': 'enabled'}]
            if tf is False:
                self.root.spec.providerSpec.value.nodeLabels += [{'key': 'openvswitch', 'value': 'enabled'},
                                                                 {'key': 'openstack-gateway', 'value': 'enabled'}]
        if self.kwargs.subtype == 'workers_oscmp':
            self.root.spec.providerSpec.value.nodeLabels = [{'key': 'openstack-compute-node', 'value': 'enabled'}]
            if tf is False:
                self.root.spec.providerSpec.value.nodeLabels.append({'key': 'openvswitch', 'value': 'enabled'})
            else:
                self.root.spec.providerSpec.value.nodeLabels.append({'key': 'tfvrouter', 'value': 'enabled'})
        if self.kwargs.subtype == 'tf_ctl':
            self.root.spec.providerSpec.value.nodeLabels = [{'key': 'tfconfig', 'value': 'enabled'},
                                                            {'key': 'tfcontrol', 'value': 'enabled'},
                                                            {'key': 'tfwebui', 'value': 'enabled'},
                                                            {'key': 'tfconfigdb', 'value': 'enabled'}]
        if self.kwargs.subtype == 'tf_nal':
            self.root.spec.providerSpec.value.nodeLabels = [{'key': 'tfanalytics', 'value': 'enabled'},
                                                            {'key': 'tfanalyticsdb', 'value': 'enabled'}]

def get_components():
    if 'hosts' in inv.parameters:
        for subtype, subtype_values in inv.parameters.hosts.items():
            yield subtype, subtype_values

def generate_manifests(input_params):
    obj = BaseObj()
    for subtype, subtype_values in get_components():
        if subtype_values.names != []:
            machines_bundle = []
            for name in subtype_values.names:
                machines = Machine(name=name, subtype=subtype)
                machines_bundle += [machines.root]
            obj.root["{}-machines".format(subtype)] = machines_bundle
    return obj

def main(input_params):
    return generate_manifests(input_params)

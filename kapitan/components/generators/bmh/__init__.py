import base64

from kapitan.inputs.kadet import BaseObj, inventory, CompileError

inv = inventory()

class Baremetalhost(BaseObj):
    def new(self):
        self.need("subtype")
        self.need("name")
        self.update_root("lib/bmh.yaml")

    def body(self):
        self.root.metadata.name = self.kwargs.name
        self.root.metadata.namespace = inv.parameters.cluster.namespace
        self.root.metadata.labels.baremetal = "bm-" + self.kwargs.name
        if self.kwargs.subtype is 'managers':
            self.root.metadata.labels['hostlabel.bm.kaas.mirantis.com/controlplane'] = 'true'
        if self.kwargs.subtype is 'workers_storage':
            self.root.metadata.labels['hostlabel.bm.kaas.mirantis.com/storage'] = 'true'
        else:
            self.root.metadata.labels['hostlabel.bm.kaas.mirantis.com/worker'] = 'true'
        self.root.metadata.labels['kaas.mirantis.com/region'] = inv.parameters.cluster.region
        self.root.spec.bootUEFI = inv.parameters.nodes[self.kwargs.name].bootUEFI
        self.root.spec.bootMACAddress = inv.parameters.nodes[self.kwargs.name].macAddress
        self.root.spec.bmc.credentialsName = self.kwargs.name
        self.root.spec.bmc.address = inv.parameters.nodes[self.kwargs.name].bmcAddress

class BaremetalhostSecret(BaseObj):
    def new(self):
        self.need("name")
        self.update_root("lib/bmh_secret.yaml")

    def body(self):
        self.root.metadata.name = self.kwargs.name + 'bmc-secret'
        self.root.metadata.namespace = inv.parameters.cluster.namespace
        self.root.metadata.labels['kaas.mirantis.com/region'] = inv.parameters.cluster.region
        self.root.metadata.labels['kaas.mirantis.com/provider'] = inv.parameters.cluster.provider
        username_bytes = inv.parameters.nodes[self.kwargs.name].bmcUsername.encode('ascii')
        username_encoded = base64.b64encode(username_bytes).decode('ascii')
        password_bytes = inv.parameters.nodes[self.kwargs.name].bmcPassword.encode('ascii')
        password_encoded = base64.b64encode(password_bytes).decode('ascii')
        self.root.data.username = username_encoded
        self.root.data.password = password_encoded 

def get_components():
    if 'hosts' in inv.parameters:
        for subtype, subtype_values in inv.parameters.hosts.items():
            yield subtype, subtype_values

def generate_manifests(input_params):
    obj = BaseObj()
    for subtype, subtype_values in get_components():
        if subtype_values.names != []:
            bmh_bundle = []
            for name in subtype_values.names:
                bmh = Baremetalhost(name=name, subtype=subtype)
                bmh_secret = BaremetalhostSecret(name=name) 
                bmh_bundle += [bmh.root]
                bmh_bundle += [bmh_secret.root]
            obj.root["{}-bmh".format(subtype)] = bmh_bundle
    return obj

def main(input_params):
    return generate_manifests(input_params)

import yaml
import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Parse hardware spreadsheet from CSV to YAML"
    )
    parser.add_argument("spreadsheet", action="store", help=("Path to spreadsheet"))
    parser.add_argument("catalogue", action="store", help=("Folder where spreadsheet will be placed"))
    return parser.parse_args()

def main():
    args = parse_args()
    df = pd.read_csv(args.spreadsheet, delimiter=',')
    #TODO: Consider moving summary to other place in spreadsheet tempalte
    sumIndex = df[df.Cluster == 'Summary'].index[0]
    df = df.iloc[:sumIndex]
    macs = df['PXE MAC']
    bmcIPs = df['BMC IP']
    bmcUsernames = df['IPMI UserName']
    bmcPasswords = df['IPMI Password']
    roles = df['Role']
    roles = roles.map({
    #NOTE: MCC mgmt and regional cluster is out of scope
    'Management Cluster Node (MCC)': 'mgmt-manager',
    'Regional Cluster Node (MCC-region)': 'region',
    'Managed Master Node (MKE)': 'child-manager',
    'Managed Worker Node (K8S worker)': 'worker',
    'Managed Worker Node (OS CP)': 'worker-ctl',
    'Managed Worker Node (OS Compute)': 'worker-cmp',
    'Managed Worker Node (OSD Node)': 'ceph',
    'Managed Worker Node (TF CTL)': 'tf-ctl',
    'Managed Worker Node (TF NAL)': 'tf-nal'
    })
    #TODO: consider using nested dict from collecion lib, such creation as below is not very ...  
    inventory = {
        'classes': ['common', 'my_component'],
        'parameters': {
            'target_name': 'rendered_target',
            'subnets': {
                'storage-access': {
                    'cidr': 'SET_ME_PROPERLY'
                },
                'storage-backend': {
                    'cidr': 'SET_ME_PROPERLY'
                },
                'tenant': {
                    'cidr': 'SET_ME_PROPERLY'
                },
                'floating': {
                    'cidr': 'SET_ME_PROPERLY'
                }
            },
            'cluster': {
                'name': 'SET_ME_PROPERLY',
                'namespace': 'SET_ME_PROPERLY',
                'region': 'SET_ME_PROPERLY',
                'provider': 'SET_ME_PROPERLY',
                'release': 'SET_ME_PROPERLY',
                'publicKey': 'SET_ME_PROPERLY',
                'metallbPool': 'SET_ME_PROPERLY',
                'loadBalancerHost': 'SET_ME_PROPERLY',
                'network': {
                    'podsCidr': 'SET_ME_PROPERLY',
                    'servicesCidr': 'SET_ME_PROPERLY'},
            },
            'nodes': {},
            'hosts': {}
        }
    }
    for i in range(bmcIPs.index.stop-1):
        inventory['parameters']['nodes'][f'node{i}-{roles[i]}'] = {
            'macAddress': macs[i],
            'bmcAddress': bmcIPs[i],
            'bootUEFI': 'false',
            'bmcUsername': bmcUsernames[i],
            'bmcPassword': bmcPasswords[i]
        }
    #TODO: Maybe we need loop here?
    inventory['parameters']['hosts']['managers'] = {'names': [f'node{i}-{roles[i]}' for i in range(roles.index.stop-1) if roles[i] == 'child-manager']}
    inventory['parameters']['hosts']['workers_generic'] = {'names': [f'node{i}-{roles[i]}' for i in range(roles.index.stop-1) if roles[i] == 'worker']}
    inventory['parameters']['hosts']['workers_storage'] = {'names': [f'node{i}-{roles[i]}' for i in range(roles.index.stop-1) if roles[i] == 'ceph']}
    inventory['parameters']['hosts']['workers_osctl'] = {'names': [f'node{i}-{roles[i]}' for i in range(roles.index.stop-1) if roles[i] == 'worker-ctl']}
    inventory['parameters']['hosts']['workers_oscmp'] = {'names': [f'node{i}-{roles[i]}' for i in range(roles.index.stop-1) if roles[i] == 'worker-cmp']}
    inventory['parameters']['hosts']['tf_ctl'] = {'names': [f'node{i}-{roles[i]}' for i in range(roles.index.stop-1) if roles[i] == 'tf-ctl']}
    inventory['parameters']['hosts']['tf_nal'] = {'names': [f'node{i}-{roles[i]}' for i in range(roles.index.stop-1) if roles[i] == 'tf-nal']}
    with open(args.catalogue + '/rendered_target.yml', 'w+') as file:
        yaml.dump(inventory, file, default_flow_style=False)

if __name__ == '__main__':
    main()

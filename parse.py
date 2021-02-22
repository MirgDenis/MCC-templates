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
    hosts = {
        'apiVersion': 'airshipit.org/v1alpha1',
        'kind': 'VariableCatalogue',
        'metadata': {
            'name': 'host-catalogue'
         },
        'hosts': {
            'm3': {}
        }
    }
    #TODO: Make copy of some base struct since only metadata.name changes
    hostGen = {
        'apiVersion': 'airshipit.org/v1alpha1',
        'kind': 'VariableCatalogue',
        'metadata': {
            'name': 'host-generation-catalogue'
         },
        'hosts': {
            'm3': {}
        }
    }
    roles = roles.map({
    #NOTE: MCC mgmt and regional cluster is out of scope
    'Management Cluster Node (MCC)': 'mgmt-manager',
    'Regional Cluster Node (MCC-region)': 'region',
    'Managed Master Node (MKE)': 'child-manager',
    'Managed Worker Node (K8S worker)': 'worker',
    'Managed Worker Node (OS CP)': 'worker-ctl',
    'Managed Worker Node (OS Compute)': 'worker-cmp',
    'Managed Worker Node (OSD Node)': 'ceph'
    })
    for i in range(bmcIPs.index.stop-1):
        hosts['hosts']['m3'][f'node{i}-{roles[i]}'] = {
            'macAddress': macs[i],
            'bmcAddress': bmcIPs[i],
            'bootUEFI': 'false',
            'bmcUsername': bmcUsernames[i],
            'bmcPassword': bmcPasswords[i]
        }
    #TODO: Maybe we need loop here?
    hostGen['hosts']['m3']['managers'] = [{'name': f'node{i}-{roles[i]}'} for i in range(roles.index.stop-1) if roles[i] == 'child-manager']
    hostGen['hosts']['m3']['workers'] = {}
    hostGen['hosts']['m3']['workers']['generic'] = [{'name': f'node{i}-{roles[i]}'} for i in range(roles.index.stop-1) if roles[i] == 'worker']
    hostGen['hosts']['m3']['workers']['storage'] = [{'name': f'node{i}-{roles[i]}'} for i in range(roles.index.stop-1) if roles[i] == 'ceph']
    hostGen['hosts']['m3']['workers']['oscontrol'] = [{'name': f'node{i}-{roles[i]}'} for i in range(roles.index.stop-1) if roles[i] == 'worker-ctl']
    hostGen['hosts']['m3']['workers']['oscompute'] = [{'name': f'node{i}-{roles[i]}'} for i in range(roles.index.stop-1) if roles[i] == 'worker-cmp']
    with open(args.catalogue + '/hosts.yaml', 'w+') as file:
        yaml.dump(hosts, file, default_flow_style=False)
    with open(args.catalogue + '/host-generation.yaml', 'w+') as file:
        yaml.dump(hostGen, file, default_flow_style=False)

if __name__ == '__main__':
    main()

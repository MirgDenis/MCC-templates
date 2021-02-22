# MCC templates
This repo is intented to simplify MCC cluster deployment and collect all
variables in one directory.

There are a few solutions fot this:
* ./manifests - soulution based on kustomize.
* ./kapitan - solution based on kapitan.

This README is for kustomize solution, kapitan README is inside `./kapitan`

## Requirements:
Docker and Kustomize >= 3.8.6

## Preparation
VariableCatalogue is yaml structure used by kustomize replacement-transformer plugin (for info check airshipctl [0] krm-functions).
MCC-templates has set of catalogues placed in `manifests/cluster/shared` directory such as:
* hosts.yaml
Catalogue describing BMC parameters for hardware nodes.  
* host-generation.yaml
Catalogue describing node roles and k8s labels for them.
* networking.yaml
Catalogue describing k8s and hardware networking.
* cluster.yaml
Catalogue describing child cluster which will be deployed.

Hosts catalogue parameters description:
* `hosts.m3.<node_name>` - name of baremetal node
* `hosts.m3.<node_name>.macAddress` - MAC of PXE interface
* `hosts.m3.<node_name>.bmcAddress` - BMC (e.g. IPMI) IP address
* `hosts.m3.<node_name>.bootUEFI` - boot mode for node (boolean)
* `hosts.m3.<node_name>.bmcUsername` - BMC username
* `hosts.m3.<node_name>.bmcPassword` - BMC password

Host-generation catalogue parameters description:
* `hosts.m3.<node_type>` - set of nodes with the same type
* `hosts.m3.<node_type>[].name` - node name, **must match with name from hosts catalogue**
* `hosts.m3.<node_type>[].BMHProfilename` - BMHProfile for machine (optional)
* `hosts.m3.<node_type>[].BMHProfile.name` - name of BMHProfile for machine
* `hosts.m3.<node_type>[].BMHProfile.namespace` - namespace of BMHProfile for machine
* `hosts.m3.<node_type>[].l2template.name` - name of l2template for machine (optional)

Possible node types:
* managers - k8s manager nodes
* workers.generic - generic k8s worker nodes
* workers.storage - storage k8s worker nodes
* workers.oscompute - k8s worker node intended to be used as Openstack compute node
* workers.oscontrol - k8s worker node intended to be used as Openstack control plane node

Networking catalogue parameters description:
* `kubernetes.serviceCidr` - CIDR for  k8s services
* `kubernetes.podCidr` - CIDR  for k8s pods
* `kubernetes.dnsNameservers` - DNS name server
* `kubernetes.loadBalancerHost` - IP of loadbalancer for k8s cluster
* `kubernetes.addressPools` - pool of IP adresses for metallb helm release
* `ipam.subnets` - subnets to generate (optional)
* `ipam.subnets.<subnet_name>` - subnet name
* `ipam.subnets.<subnet_name>.cidr` - CIDR for subnet
* `ipam.l2template` - l2template (optional)
* `ipam.l2template.name` - name of l2template
* `ipam.l2template.autoIfMappingPrio` - priority of automatic interface mapping
* `ipam.l2template.template` - netplan template

Cluster catalogue parameters description:
* `commonCluster.clusterName` - name of child cluster
* `commonCluster.release` - cluster release
* `commonCluster.publicKeyName` - name of SSH key for cluster
* `commonCluster.publicKey` - SSH key for cluster

To set common namespace or labels for all rendered manifests, change namespace
or commonLabel field in `manifests/cluster/kustomization.yaml` file.

## Hardware spreadsheet parsing

For parsing hardware spreadsheet you can use parse.py script.

### Requirements:
Python 3.6 and pandas package installed

### Use:
Export hardware list to csv and define it as spreadsheet_path and define resulting_dir as `manifests/cluster/shared` or other if you do not want to mess up current state of shared folder.

```python3 parse.py spreadsheet_path resulting_dir```

## Quickstart
``` sudo bash -x run.sh ```

It will download kustomize 3.8.6, set KUSTOMIZE_PLUGIN_HOME variable and build
configuration per contents of kustomization.yaml from manifests.

## Links
[0] - github.com/airshipit/airshipctl

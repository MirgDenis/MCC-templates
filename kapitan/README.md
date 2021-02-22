## Requirements
Kapitan installed https://github.com/kapicorp/kapitan#quickstart

## Quickstart
`kapitan c` - compile target.

Then you can find `compiled` directory was created, and within `compiled/my_target` directory rendered manifests are stored.

## Values

If you want to modify manifests you need to edit target parameters in `./inventory/targets/my_target.yml`.
| Value                                         | Description                                            |
| --------------------------------------------- |:------------------------------------------------------:|
| `cluster.name`                                | Cluster name                                           |
| `cluster.namespace`                           | Cluster namespace                                      |
| `cluster.provider`                            | Cluster provider                                       |
| `cluster.region`                              | Cluster region                                         |
| `cluster.release`                             | Cluster release                                        |
| `cluster.publicKey`                           | Public key for cluster                                 |
| `cluster.metallbPool`                         | Pool of addresses for MetalLB (e.g. 10.0.0.1-10.0.0.2) |
| `cluster.loadBalancerHost`                    | Address for K8s                                        |
| `cluster.network.podsCidr`                    | CIDR for pods in k8s                                   |
| `cluster.network.servicesCidr`                | CIDR for services in k8s                               |
| `cluster.stacklight`                          | Configure stacklight                                   |
| `cluster.stacklight.HAEnabled`                | HAEnabled (boolean)                                    |
| `cluster.stacklight.loggingEnabled`           | loggingEnabled (boolean)                               |
| `cluster.stacklight.emailAlert`               | Configure email alerting                               |
| `cluster.stacklight.emailAlert.send_resolved` | Send resolved alerts or not (boolean)                  |
| `cluster.stacklight.emailAlert.require_tls`   | Require TLS or not (boolean)                           |
| `cluster.stacklight.emailAlert.auth_identity` | Email auth identity                                    |
| `cluster.stacklight.emailAlert.auth_password` | Email auth password                                    |
| `cluster.stacklight.emailAlert.auth_secret`   | Email auth secret                                      |
| `cluster.stacklight.emailAlert.auth_username` | Email auth username                                    |
| `cluster.stacklight.emailAlert.from`          | From email address                                     |
| `cluster.stacklight.emailAlert.to`            | To email address                                       |
| `cluster.stacklight.emailAlert.smarthost`     | Email smarthost                                        |
| `hosts.<host_group>`                          | Grouped hosts, arbitrary name is possible, but groups as worker_osctl, worker_oscmp, worker_storage have predefined fileds in manifests.                          |
| `hosts.<host_group>.names`                    | List of host names, must match names from nodes field  |
| `hosts.<host_group>.nodeLabels`               | List of node labels for group of hosts (optional)      |
| `hosts.<host_group>.BMHProfile.name`          | Name of BMHProfile for group of hosts (optional)       |
| `hosts.<host_group>.BMHProfile.namespace`     | Namespace of BMHProfile for group of hosts (optional)  |
| `hosts.<host_group>.l2template.name`          | Name of l2template for group of hosts (optional)       |
| `nodes.<node_name>.macAddress`                | MAC address of boot NIC                                |
| `nodes.<node_name>.bmcAddress`                | BMC address                                            |
| `nodes.<node_name>.bootUEFI`                  | Boot UEFI mode (boolean)                               |
| `nodes.<node_name>.bmcUsername`               | BMC username                                           |
| `nodes.<node_name>.bmcPassword`               | BMC password                                           |
| `subnets.<subnet_name>.cidr`                  | CIDR for subnet (optional)                             |


## Spreadsheet parsing
Export hardware spreadshhet as csv and pass it to script.

`python3 parse.py <spreadshhet_name> <resulting_path>`

In resultinh inventory you need to set cluster parameters with SET_ME_PROPERLY placeholders.

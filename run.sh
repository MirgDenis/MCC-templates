#!/bin/sh
set -xe

if [ ! -f ./kustomize ]; then
  curl -fsSL https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv3.8.6/kustomize_v3.8.6_linux_amd64.tar.gz -o x.tar.gz && tar -zxvf x.tar.gz && rm x.tar.gz
fi

KUSTOMIZE_PLUGIN_HOME=$(pwd)/manifests ./kustomize build --enable_alpha_plugins manifests/cluster > AIO.yaml

#!/usr/bin/env python

import kopf
import kubernetes
import os

if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount/namespace'):
    kubernetes.config.load_incluster_config()
    namespace = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read()
else:
    kubernetes.config.load_kube_config()
    namespace = kubernetes.config.list_kube_config_contexts()[1]['context']['namespace']

core_v1_api = kubernetes.client.CoreV1Api()
custom_objects_api = kubernetes.client.CustomObjectsApi()

def handle_deployment(deployment, logger):
    logger.info(deployment['metadata']['name'])

@kopf.on.event('apps', 'v1', 'deployments')
def watch_deployments(event, logger, **_):
    '''
    Watch deployments
    '''
    if event['type'] in ['ADDED', 'MODIFIED', None]:
        deployment = event['object']
        handle_deployment(deployment, logger)
    elif event['type'] == 'DELETED':
        # Nothing to do on delete.
        pass
    else:
        logger.warning('Unhandled event %s', event)

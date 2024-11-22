#!/usr/bin/env python
import maltoolbox
from maltoolbox.language import LanguageClassesFactory
from maltoolbox.language import LanguageGraph
from maltoolbox.attackgraph import AttackGraph

from maltoolbox.model import Model as malmodel
from maltoolbox.ingestors import neo4j

import json
import sys

#aws_output_json = open('./aws_output.json', 'r', newline='')
aws_output_json = open(sys.argv[1], 'r', newline='')
aws_output = json.loads(aws_output_json.read())
aws_output_json.close()

lang_file = './org.mal-lang.examplelang-1.0.0.mar' # malc produces .mar files
lang_graph = LanguageGraph.from_mar_archive(lang_file)
lang_classes_factory = LanguageClassesFactory(lang_graph)

model = malmodel('AWS instances model', lang_classes_factory)

for instance_group in aws_output:
    for single_instance in instance_group:
        host = single_instance.get("Name",single_instance["Instance"])
        subnet = single_instance.get("Subnet")
        host_asset = lang_classes_factory.ns.Host(name = host)
        subnet_asset = lang_classes_factory.ns.Network(name = subnet)

        user_asset = lang_classes_factory.ns.User(name = "root")
        password_asset = lang_classes_factory.ns.Password(name = "root")

        model.add_asset(host_asset)
        model.add_asset(subnet_asset)
        model.add_association(lang_classes_factory.ns.NetworkAccess(hosts = [host_asset], networks = [subnet_asset]))

        model.add_asset(user_asset)
        model.add_asset(password_asset)
        model.add_association(lang_classes_factory.ns.Credentials_User_Password(user = [user_asset], passwords = [password_asset]))
        model.add_association(lang_classes_factory.ns.Credentials_Host_Password(host = [host_asset], passwords = [password_asset]))
model.save_to_file('aws_model.json')
graph = AttackGraph(lang_graph, model)
graph.attach_attackers()
graph.save_to_file('attack_graph.json')

""" # My local Neo4J creds
maltoolbox.neo4j_configs['uri'] = 'bolt://localhost:7687'
maltoolbox.neo4j_configs['username'] = ''
maltoolbox.neo4j_configs['password'] = ''
maltoolbox.neo4j_configs['dbname'] = 'neo4j'

# Dump to Neo4J
neo4j.ingest_model(model,
    maltoolbox.neo4j_configs['uri'],
    maltoolbox.neo4j_configs['username'],
    maltoolbox.neo4j_configs['password'],
    maltoolbox.neo4j_configs['dbname'],
    delete=True)

# Comment out this block to skip the big attack graph.
neo4j.ingest_attack_graph(graph,
    maltoolbox.neo4j_configs['uri'],
    maltoolbox.neo4j_configs['username'],
    maltoolbox.neo4j_configs['password'],
    maltoolbox.neo4j_configs['dbname'],
    delete=False)
 """


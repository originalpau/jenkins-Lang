import maltoolbox
from maltoolbox.language import LanguageClassesFactory
from maltoolbox.language import LanguageGraph
from maltoolbox.attackgraph import AttackGraph
from maltoolbox.wrappers import create_attack_graph

from maltoolbox.model import Model as malmodel
from maltoolbox.ingestors import neo4j

import json

'''
Set up en2720 exampleLang json

'''

en2720_example = open('./en2720_exampleLang.json', 'r', newline='')
en2720_example_json = json.loads(en2720_example.read())

'''
Boilerplate for loading coreLang via the toolbox.

'''
lang_file = './org.mal-lang.examplelang-1.0.0.mar' # malc produces .mar files
lang_graph = LanguageGraph.from_mar_archive(lang_file)
lang_classes_factory = LanguageClassesFactory(lang_graph)

'''
Set up en2720 model.

'''
model = malmodel('Simple EN2720 exampleLang model', lang_classes_factory)


'''
Build EN2720 exampleLang models here

'''

hosts = {}
users = {}
networks = {}
pwds = {}

for i in en2720_example_json['instances']:
    hosts[i] = lang_classes_factory.ns.Host(name = i)
    model.add_asset(hosts[i])

for u in en2720_example_json['users']:
    users[u] = lang_classes_factory.ns.User(name = u)
    model.add_asset(users[u])
    pwds[u] = lang_classes_factory.ns.Password(name = u)
    model.add_asset(pwds[u])

for n in en2720_example_json['networks']:
    networks[n] = lang_classes_factory.ns.Network(name = n)
    model.add_asset(networks[n])

for n,i in en2720_example_json['networks'].items():
    for instance in i:
        host_net_assoc  =\
            lang_classes_factory.ns.NetworkAccess(
            hosts = [hosts[instance]],
            networks = [networks[n]]
            )
        model.add_association(host_net_assoc)

for p in pwds:
    user_pw_assoc  =\
        lang_classes_factory.ns.Credentials_User_Password(
        user = [users[p]],
        passwords = [pwds[p]]
        )
    model.add_association(user_pw_assoc)

for i,v in en2720_example_json['instances'].items():
    for user in v:
        host_pw_assoc =\
                lang_classes_factory.ns.Credentials_Host_Password(
                host = [hosts[i]],
                passwords = [pwds[user]]
                )
        model.add_association(host_pw_assoc)

'''
Save models as JSON.

'''
model.save_to_file('simple_en2720_model.json')
#graph = create_attack_graph(lang_graph, model)
graph = AttackGraph(lang_graph, model)
#graph.attach_attackers(model)
graph.attach_attackers()
graph.save_to_file('simple_en2720_attack_graph.json')

'''
Neo4J boilerplate.

The Neo4J config can be under maltoolbox/default.conf.

'''
# My local Neo4J creds
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

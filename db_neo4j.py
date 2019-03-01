from py2neo import Graph, Node, Relationship, NodeMatcher
from typing import Union
from utils import load_json
from main import *

def create_graph(   bolt:Union[bool, None]=None, 
                    secure:bool=False, 
                    host:str="localhost", 
                    http_port:int=7473, 
                    https_port:int=7474, 
                    bolt_port:int=7687, 
                    user:str="neo4j", 
                    password:str="neo4j"
                ) -> Graph:

    graph = Graph(bolt=bolt, secure=secure, host=host, http_port=http_port, https_port=https_port, bolt_port=bolt_port, user=user, password=password)
    return graph

if __name__ == '__main__':
    cities = load_json("cities.json")
    city_json = get_city_json(cities)
    mp_json = get_mp_json(cities)
    party_json = get_party_json(cities)

    graph = create_graph(password="a51v63r82e92f95")

    # create city nodes
    for city in city_json:
        city_node = Node("City", **city)
        graph.create(city_node)

    # create mp nodes
    for mp in mp_json:
        mp_node = Node("MP", **mp)
        graph.create(mp_node)

    # create party nodes
    for party in party_json:
        party_node = Node("Party", **party)
        graph.create(party_node)

    # create IS_MEMBER_OF and IS_FROM relationships

    matcher = NodeMatcher(graph)
    mp_matched = matcher.match("MP")

    for mp in mp_matched:
        # IS_MEMBER_OF
        party_matched = matcher.match("Party", name=mp["party"])
        party = party_matched.first()
        rel_party = Relationship(mp, "IS_MEMBER_OF", party)
        graph.create(rel_party)
        # IS_FROM
        city_matched = matcher.match("City", name=mp["city"])
        city = city_matched.first()
        rel_city = Relationship(mp, "IS_MP_FROM", city)
        graph.create(rel_city)
#Autor: Maria Queralt Sosa Mompel
#Asignatura: Generación Automática de Código
#Practica 1: Generador automático para generar una representación gráfica a partir de un fichero XML

import xml.etree.ElementTree as ET
import sys
import os.path
import networkx as nx

G = nx.Graph()
count = 0

def search_in_tree(father,fatherid):
    global count
    for elem in father:
        count += 1
        nodeLabel = elem.tag
        if len(elem)==0 and elem.text is not None: # Si es nodo hoja mostramos el valor de su clave
            nodeLabel += ": " + elem.text
        nodeLabel+="\n"
        for attrib in elem.attrib: #Si el nodo tiene atributos los representamos
            nodeLabel += attrib + ": " + elem.attrib[attrib] + "\n"
        G.add_nodes_from([("n"+str(count), {"data": nodeLabel })]) # añadimos nuevo nodo
        G.add_edge(fatherid, "n"+str(count), label=nodeLabel) #creamos un borde
        if len(elem)>0: # Si no se trata de un nodo hoja seguimos recorriendo los sucesivos hijos del nodo padre actual
            search_in_tree(elem,"n"+str(count))

def read_xml_file(path):
    if (os.path.exists(path)):
        try:
            tree = ET.parse(path)
            root = tree.getroot() #obtenemos un árbol iterable
            G.add_nodes_from([("n0", {"data": root.tag })]) #añadimos el nodo padre raíz
            search_in_tree(root,"n0")
            nx.write_graphml_lxml(G,"generator2-results.graphml", encoding='UTF-8')
            print("Successful compilation, see the results in generator2-results.graphml")

        except ET.ParseError as error:
            print("XML Parse Error caused by " + error.msg)
    else:
        print("File path not found")

if len(sys.argv) == 1:
    print("You must introduce a real XML file path too")
else:
    path = sys.argv[1]
    if (path.__contains__(".xml")):
        read_xml_file(path)
    else:
        print("You must introduce a real XML file path")
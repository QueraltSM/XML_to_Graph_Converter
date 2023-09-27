#Autor: Maria Queralt Sosa Mompel
#Asignatura: Generación Automática de Código
#Practica 1: Generador automático para generar un objeto JSON a partir de un fichero XML

import xml.etree.ElementTree as ET
import sys
import os.path

file = open("generator1-results.txt", mode='w', encoding='UTF-8') #Para evitar error UnicodeEncodeError: 'charmap' codec can't encode characters
main_nodes = [] 
tabulations = 0

def print_tab(t):
    global tabulations
    tabulations += t
    for i in range(tabulations):
        file.write("\t")

def remove_extra_space_and_linebreaks(s): #Eliminamos posibles saltos de líneas y espacios innecesarios
    if s is None:
        return ""
    else:
        return " ".join(''.join(s.splitlines()).split())

def search_in_tree(father):
    main_nodes = []
    for node in father:
        if node.tag not in main_nodes and len(node)>0: # Bloque para evitar que mismo tag se repita en el objeto JSON
            main_nodes.append(node.tag)
            print_tab(1)

            if len(father.findall(node.tag))>1: #Existen varios nodos con la misma etiqueta
                file.write('"' + node.tag + '": [\n')
                print_tab(1)
                file.write('{\n')
            else: #Existe sólo un nodo con la misma etiqueta
                file.write('"' + node.tag + '": {\n')

        elif len(father.findall(node.tag))>1: # Concatenamos con llave si existen varios nodos hijos con mismo tag
            print_tab(1)
            file.write('{\n')
        
        if len(node)==0 and len(node.attrib)==0: # Representamos la informacion de un nodo hoja
            print_tab(1)
            file.write('"' + node.tag+'": "' + remove_extra_space_and_linebreaks(node.text) + '"')
        elif len(node)==0 and len(node.attrib)>0:
            print_tab(1)
            file.write('"' + node.tag + '": {\n')
            print_tab(1)
            for attrib in node.attrib: #Nodo tiene atributos
                file.write('"_' + attrib +'": "' + remove_extra_space_and_linebreaks(node.attrib[attrib]) + '",\n')
                print_tab(0)
            file.write('"__text": "' + remove_extra_space_and_linebreaks(node.text) + '"\n')
            print_tab(-1)
            file.write("}")
        else: # Seguimos recorriendo el árbol hasta buscar un nodo hoja
            search_in_tree(node)

        if len(node)>0 and len(node.attrib)>0:
            file.seek(file.tell() - 2, os.SEEK_SET) #Añadimos coma después de cerrar objeto en caso de que su padre tenga atributos
            file.write(",\n")
            for attrib in node.attrib: #Nodo tiene atributos
                print_tab(0)
                file.write('"_' + attrib +'": "' + remove_extra_space_and_linebreaks(node.attrib[attrib]) + '"')
                if (attrib != list(node.attrib)[-1]): #Se concatenan los attributos con comas, excepto el último de ellos
                    file.write(",")  
                file.write("\n") 

        if len(father.findall(node.tag))>1: # Hijos misma etiqueta termina en llave
            print_tab(-1) 
            file.write("}")
        
        if len(father.findall(node.tag))>1 and node == father.findall(node.tag)[-1] and len(node)>0: #Existen varios nodos con la misma etiqueta finaliza en corchete
            file.write("\n")
            print_tab(-1)
            file.write("]")
        elif node == father.findall(node.tag)[-1] and len(node)>0: #Existe sólo un nodo con la misma etiqueta finaliza en llaves
            print_tab(-1)
            file.write("}")
   
        if node != father[-1]: #Concatenamos con una coma las claves y valores de los nodos
            file.write(",")
            print_tab(-1)

        file.write("\n") # Saltamos de línea para seguir construyendo el objeto JSON

def read_xml_file(path):
    if (os.path.exists(path)):
        try:
            tree = ET.parse(path) # Parseamos el contenido del fichero XML con la API
            root = tree.getroot() # Obtenemos un árbol iterable
            file.write("{\n") # Abrimos siempre el objeto json con una llave
            print_tab(1)
            file.write('"'+root.tag+'": {',) # Empezamos a escribir en el fichero destino el nombre del padre/raiz y una llave
            file.write("\n")
            search_in_tree(root)
            print_tab(-1)
            file.write("}\n")
            file.write("}") # Cerramos siempre el objeto json con una llave
            print("Successful compilation, see the results in generator1-results.txt")
        except ET.ParseError as error:
            print("XML Parse Error caused by " + error.msg)
            file.write("null")
    else:
        print("File path not found")
        file.write("null")

path = sys.argv[1]
if (path.__contains__(".xml")):
    read_xml_file(path)
else:
    print("You must introduce a real XML file path")
    file.write("null")
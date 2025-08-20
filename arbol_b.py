from collections import deque
from math import ceil
from operator import attrgetter

class Proveedor:
    def __init__(self, id, nombre, tipo_servicio, calificacion, ubicacion):
        self.id = id
        self.nombre = nombre
        self.tipo_servicio = tipo_servicio
        self.calificacion = calificacion
        self.ubicacion = ubicacion

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Servicio: {self.tipo_servicio}, Calificación: {self.calificacion}, Ubicación: {self.ubicacion}"

    def __repr__(self):
        return self.__str__()

class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []

    def insert(self, proveedor):
        if self.leaf:
            self.keys.append(proveedor)
            self.keys.sort(key=lambda x: x.id)
        else:
            i = 0
            while i < len(self.keys) and proveedor.id > self.keys[i].id:
                i += 1
            
            if i < len(self.children):
                self.children[i].insert(proveedor)
            else:
                new_child = BTreeNode(leaf=True)
                new_child.insert(proveedor)
                self.children.append(new_child)

    def traverse_inorder(self):
        result = []
        for i in range(len(self.keys)):
            if i < len(self.children):
                result.extend(self.children[i].traverse_inorder())
            result.append(self.keys[i])
        
        if len(self.children) > len(self.keys):
            result.extend(self.children[-1].traverse_inorder())
        
        return result

    def search_by_service(self, tipo_servicio):
        results = []
        for key in self.keys:
            if key.tipo_servicio.lower() == tipo_servicio.lower():
                results.append(key)
        
        for child in self.children:
            results.extend(child.search_by_service(tipo_servicio))
        
        return results

class BTree:
    def __init__(self, order=4):
        self.order = order
        self.root = BTreeNode(leaf=True)

    def insert(self, proveedor):
        if len(self.root.keys) >= self.order:
            old_root = self.root
            self.root = BTreeNode(leaf=False)
            self.root.children.append(old_root)
            self._split_child(self.root, 0)
        
        self._insert_non_full(self.root, proveedor)

    def _insert_non_full(self, node, proveedor):
        if node.leaf:
            # Insertar en nodo hoja
            node.keys.append(proveedor)
            node.keys.sort(key=lambda x: x.id)
        else:
            i = 0
            while i < len(node.keys) and proveedor.id > node.keys[i].id:
                i += 1
            
            if len(node.children[i].keys) >= self.order:
                self._split_child(node, i)
                if proveedor.id > node.keys[i].id:
                    i += 1
            
            self._insert_non_full(node.children[i], proveedor)

    def _split_child(self, parent, child_index):
        child = parent.children[child_index]
        new_child = BTreeNode(leaf=child.leaf)
        
        mid = len(child.keys) // 2
        new_child.keys = child.keys[mid + 1:]
        child.keys = child.keys[:mid]
        
        if not child.leaf:
            new_child.children = child.children[mid + 1:]
            child.children = child.children[:mid + 1]
        
        parent.keys.insert(child_index, child.keys.pop())
        parent.children.insert(child_index + 1, new_child)

    def traverse_inorder(self):
        print("Listado de Proveedores:")
        if len(self.root.keys) == 0:
            print("El árbol está vacío.")
        else:
            all_proveedores = self.root.traverse_inorder()
            for proveedor in all_proveedores:
                print(proveedor)
        print()

    def search_by_service(self, tipo_servicio):
        if len(self.root.keys) == 0:
            return []
        results = self.root.search_by_service(tipo_servicio)
        results.sort(key=attrgetter("calificacion"), reverse=True)
        return results

    def display(self):
        print("Visualización del árbol por niveles:")
        if len(self.root.keys) == 0:
            print("El árbol está vacío.")
        else:
            self._display_recursive(self.root, 0)

    def _display_recursive(self, node, level):
        print(f"Nivel {level}: {[p.id for p in node.keys]}")
        for child in node.children:
            self._display_recursive(child, level + 1)
    


    
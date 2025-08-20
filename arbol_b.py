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
    def __init__(self, t, leaf=False):
        self.t = t 
        self.leaf = leaf
        self.keys = []
        self.children = []

    # MÉTODO INSERTAR (no lleno)
    def insert_non_full(self, proveedor):
        i = len(self.keys) - 1
        
        if self.leaf:
            self.keys.append(None)
            while i >= 0 and proveedor.id < self.keys[i].id:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = proveedor
        else:
            while i >= 0 and proveedor.id < self.keys[i].id:
                i -= 1
            i += 1
            
            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i)
                if proveedor.id > self.keys[i].id:
                    i += 1
                    
            self.children[i].insert_non_full(proveedor)

    def split_child(self, i):
        t = self.t
        y = self.children[i]
        z = BTreeNode(t, y.leaf)
        
        z.keys = y.keys[t:]
        y.keys = y.keys[:t-1]
        
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]
        
        self.keys.insert(i, y.keys.pop())
        self.children.insert(i + 1, z)

    # MÉTODO MOSTRAR (recorrido inorden)
    def traverse_inorder(self):
        for i in range(len(self.keys)):
            if not self.leaf:
                self.children[i].traverse_inorder()
            print(self.keys[i])
        if not self.leaf:
            self.children[len(self.keys)].traverse_inorder()

    # MÉTODO BUSCAR (por servicio)
    def search_by_service(self, tipo_servicio):
        results = []
        for key in self.keys:
            if key.tipo_servicio.lower() == tipo_servicio.lower():
                results.append(key)
        
        if not self.leaf:
            for child in self.children:
                results.extend(child.search_by_service(tipo_servicio))
        
        return results

    def collect_levels(self):
        result = []
        queue = deque([(self, 0)])
        while queue:
            node, level = queue.popleft()
            if len(result) <= level:
                result.append([])
            
            result[level].append([p.id for p in node.keys])
            
            for child in node.children:
                queue.append((child, level + 1))
        return result

class BTree:
    def __init__(self, m):
        self.order = m
        self.t = ceil(m / 2)
        self.root = BTreeNode(self.t, True)

    # MÉTODO INSERTAR PRINCIPAL
    def insert(self, proveedor):
        root = self.root
        
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t, False)
            new_root.children.append(self.root)
            new_root.split_child(0)
            
            i = 0
            if proveedor.id > new_root.keys[0].id:
                i = 1
            new_root.children[i].insert_non_full(proveedor)
            
            self.root = new_root
        else:
            self.root.insert_non_full(proveedor)

    # MÉTODO MOSTRAR PRINCIPAL
    def traverse_inorder(self):
        print("Listado de Proveedores:")
        self.root.traverse_inorder()
        print()

    def display(self):
        print("Visualización del árbol por niveles:")
        levels = self.root.collect_levels()
        for i, level_nodes in enumerate(levels):
            print(f"Nivel {i}: ", end="")
            for node_keys in level_nodes:
                print(f"{node_keys} ", end="")
            print()

    # MÉTODO BUSCAR PRINCIPAL
    def search_by_service(self, tipo_servicio):
        results = self.root.search_by_service(tipo_servicio)
        results.sort(key=attrgetter("calificacion"), reverse=True)
        return results
    


    
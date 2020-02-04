# encoding:utf-8

import pickle
import tornado.web
import os,stat

class ADHandler(tornado.web.RequestHandler):
    
    with open("knowledge_graphs/data/graphPkl.pkl", "rb") as f:
        data = pickle.load(f)
        graph = data[list(data.keys())[0]]

    def get(self):
        self.render("jiezhichangai_graph.html")

    def post(self):
        print(len(self.graph["edges"]))
        self.write(self.graph)























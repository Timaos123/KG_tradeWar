# encoding:utf-8

import pickle
import tornado.web
import os,stat
import searchByKWGraph as sbkg

class ADHandler(tornado.web.RequestHandler):

    
    def get(self):
        kw=self.get_argument("kw","zte")
        sbkg.main(kw)
        self.render("jiezhichangai_graph.html")

    def post(self):
        with open("knowledge_graphs/data/searchGraphPkl.pkl", "rb") as f:
            data = pickle.load(f)
        graph = data[list(data.keys())[0]]
        # print(len(self.graph["edges"]))
        self.write(graph)























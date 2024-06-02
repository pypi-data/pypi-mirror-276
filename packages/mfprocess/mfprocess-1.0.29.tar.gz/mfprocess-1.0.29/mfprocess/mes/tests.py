from pyvis.network import Network


def get_html():
  net = Network()
  rels = [
      
      ["Fred", "George"],
      ["Harry", "Rita"],
      ["Fred", "Ginny"],
      ["Tom", "Ginny"],
      ["Harry", "Ginny"]
      
  ]
  
  for rel in rels:
      source, dest = rel
      net.add_node(source)
      net.add_node(dest)
      net.add_edge(source, dest)
  # net.toggle_physics(False)
  return net.generate_html()

def save_html():
  net = Network()
  rels = [
      
      ["Fred", "George"],
      ["Harry", "Rita"],
      ["Fred", "Ginny"],
      ["Tom", "Ginny"],
      ["Harry", "Ginny"]
      
  ]
  
  for rel in rels:
      source, dest = rel
      net.add_node(source)
      net.add_node(dest)
      net.add_edge(source, dest)
  net.toggle_physics(False)
  net.save_graph("graph.html")
  return None

def param_get_html():
  df=pd.read_csv('data.csv')
  rels = df.to_numpy().tolist()
  
  for rel in rels:
      source, dest = rel
      net.add_node(source)
      net.add_node(dest)
      net.add_edge(source, dest)
  net.toggle_physics(False)
  return net.generate_html()

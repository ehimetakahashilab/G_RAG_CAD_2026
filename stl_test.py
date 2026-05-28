import trimesh

mesh = trimesh.load('example.stl', force='mesh')

print("頂点数:", len(mesh.vertices))
print("面数:", len(mesh.faces))
print("体積:", mesh.volume)
print("表面積:", mesh.area)
print("バウンディングボックス:", mesh.bounds)
print("重心:", mesh.center_mass)
print("接続された部品数:", len(mesh.split()))

# Fundanur Öztürk
# 21118080056

import networkx as nx
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

# Grafik oluştur
# Öğrencileri temsil eden bir grafik (Graph) oluşturuyoruz.
G = nx.Graph()

# 10 adet düğüm (öğrenci) oluştur
# Düğümler "n1" ile "n10" arasında isimlendirilmiş
nodes = [f"n{i}" for i in range(1, 11)]
G.add_nodes_from(nodes)  # Grafiğe düğümleri ekliyoruz

# Rastgele 15 bağlantı (arkadaşlık ilişkisi) ekle
for _ in range(15):
    u = random.choice(nodes)  # Rastgele bir düğüm seç
    v = random.choice(nodes)  # Başka bir rastgele düğüm seç
    if u != v:  # Kendisiyle bağlantı olmaması için kontrol
        G.add_edge(u, v)  # İki düğüm arasında bir bağlantı ekle

# Popülerlik analizi
# Her düğümün bağlantı sayısını (derecesini) hesaplıyoruz
popularity = {node: G.degree(node) for node in G.nodes()}

# En popüler düğümü (en çok bağlantısı olan) buluyoruz
most_popular = max(popularity, key=popularity.get)
print(f"En popüler öğrenci: {most_popular}, arkadaş sayısı: {popularity[most_popular]}")

# Bağlantısı olmayan düğüm çiftlerini bul
unconnected_nodes = [
    (u, v) for u in nodes for v in nodes if u != v and not G.has_edge(u, v)
]
if unconnected_nodes:
    # Yapay zeka önerisi: rastgele bir düğüm çifti öner
    suggested_pair = random.choice(unconnected_nodes)
    print(f"Yapay zeka önerisi: {suggested_pair[0]} ile {suggested_pair[1]} arkadaş olabilir.")

# Ortak komşu sayısına göre arkadaş önerileri
# Bir düğüm için öneri yapacak fonksiyon tanımlıyoruz
def suggest_friend(G, node):
    suggestions = {}
    for other in G.nodes():  # Tüm düğümleri dolaş
        if node != other and not G.has_edge(node, other):
            # Ortak komşu sayısını hesapla
            common_neighbors = len(list(nx.common_neighbors(G, node, other)))
            if common_neighbors > 0:  # Ortak komşu varsa öneriye ekle
                suggestions[other] = common_neighbors
    # Ortak komşu sayısına göre azalan sırada sıralıyoruz
    return sorted(suggestions.items(), key=lambda x: x[1], reverse=True)

# Merkezilik analizi
# Derece merkeziliği ölçümü (bir düğümün toplam bağlantı sayısı)
degree_centrality = nx.degree_centrality(G)
most_important = max(degree_centrality, key=degree_centrality.get)
print(f"En önemli düğüm (derece merkeziliği): {most_important}")

# Betweenness merkeziliği ölçümü (bilgi akışı üzerindeki kritik düğümler)
betweenness_centrality = nx.betweenness_centrality(G)
most_central = max(betweenness_centrality, key=betweenness_centrality.get)
print(f"En merkezi düğüm (betweenness merkeziliği): {most_central}")

# Topluluk tespiti
# Grafikteki düğümleri topluluklara ayırıyoruz
# greedy_modularity_communities, bağlantı yapısına göre toplulukları bulur
top_communities = list(nx.algorithms.community.greedy_modularity_communities(G))

# Toplulukları renklendirme
colors = ["red", "blue", "green", "orange"]  # Her topluluk için bir renk
color_map = []
for node in G:
    for i, community in enumerate(top_communities):
        if node in community:  # Düğüm hangi toplulukta?
            color_map.append(colors[i % len(colors)])

# Animasyon
# Grafiği düzenlemek için bir düzen (layout) belirliyoruz
pos = nx.spring_layout(G)
fig, ax = plt.subplots()  # Çizim için figür ve eksen oluştur

# Her karede (frame) grafiği güncelleyen bir fonksiyon tanımlıyoruz
def update(frame):
    ax.clear()  # Eski çizimi temizle

    # Rastgele iki düğüm seç ve aralarında bağlantı ekle
    u, v = random.choice(nodes), random.choice(nodes)
    if u != v and not G.has_edge(u, v):
        G.add_edge(u, v)

    # Öneri sistemini güncelle
    node = random.choice(nodes)  # Rastgele bir düğüm seç
    suggestions = suggest_friend(G, node)  # Önerileri al

    # Merkezilik ölçümlerini güncelle
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

    # Düğümleri renklendir
    node_colors = []
    for n in G.nodes():
        if n == most_important:
            node_colors.append('red')  # En önemli düğüm
        elif n == most_central:
            node_colors.append('green')  # En merkezi düğüm
        else:
            node_colors.append(color_map[nodes.index(n)])  # Topluluk renkleri

    # Grafiği çiz
    nx.draw(
        G, pos, with_labels=True, node_color=node_colors, node_size=800, font_weight="bold"
    )

    # Önerileri görselleştir
    if suggestions:
        suggestion_text = f"{node} için öneriler: {', '.join([f'{s[0]} ({s[1]})' for s in suggestions])}"
    else:
        suggestion_text = f"{node} için öneri yok."

    # Başlıkta önerileri göster
    ax.set_title(f"Frame: {frame}\n{suggestion_text}")

# Animasyonu başlat
ani = animation.FuncAnimation(fig, update, frames=10, interval=1000, repeat=False)
plt.show()

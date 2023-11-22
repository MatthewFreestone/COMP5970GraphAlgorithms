from manim import *

class Bipartite(Scene):

    def getEdges(self, idx_to_node, edges):
        actual_lines = []
        for u, v, d in edges:
            label = Text(str(d['weight']), font_size=24)
            l = LabeledLine(label=label, start=idx_to_node[u], end=idx_to_node[v], label_position=0.2, label_frame=False)
            actual_lines.append(l)
        # print(actual_lines)
        return actual_lines
    
    def construct(self):
        nodes = [Circle(fill_opacity=0.8, fill_color='RED').scale(0.3) for _ in range(8)]
        left = nodes[:5]
        lvg = VGroup(*left).arrange(UP, buff=0.6).shift(3*LEFT)

        right = nodes[5:]
        for n in right:
            n.color = "BLUE"
        rvg = VGroup(*right).arrange(UP, buff=0.5).shift(3*RIGHT)

        edges = [(0, 5, {'weight': 3}), (0, 7, {'weight': 1}), (1, 5, {'weight': 4}), (1, 6, {'weight': 8}), (2, 6, {'weight': 1}), (2, 7, {'weight': 3}), (3, 5, {'weight': 6}), (3, 6, {'weight': 2}), (4, 5, {'weight': 5}), (4, 6, {'weight': 6}), (4, 7, {'weight': 3})]
        lines = VGroup(*self.getEdges(nodes, edges))
        self.add(Text('Maximum Weighted Bipartite Matching', font_size=36).align_on_border(UP))
        self.play(FadeIn(lvg))
        self.play(FadeIn(rvg))
        self.play(Create(lines))



        step1 = Text('1. Add fake nodes to allow perfect matching', font_size=30).align_on_border(DOWN)
        self.play(Create(step1))

        fake_nodes = [Circle(fill_opacity=0.3, color="BLUE").scale(0.3) for _ in range(2)]
        old_right = [Circle(fill_opacity=0.8, color="BLUE").scale(0.3) for _ in right]
        n_rvg = VGroup(*(fake_nodes + old_right)).arrange(UP, buff=0.6).shift(3*RIGHT)

        idx_to_node = {i:v for i,v in enumerate(left)}
        idx_to_node.update({i+len(left): v for i,v in enumerate(old_right)})
        for i,v in enumerate(fake_nodes):
            idx_to_node[f'FAKE_NODE_{i}'] = v

        edges = [(0, 5, {'weight': 3}), (0, 7, {'weight': 1}), (1, 5, {'weight': 4}), (1, 6, {'weight': 8}), (2, 6, {'weight': 1}), (2, 7, {'weight': 3}), (3, 5, {'weight': 6}), (3, 6, {'weight': 2}), (4, 5, {'weight': 5}), (4, 6, {'weight': 6}), (4, 7, {'weight': 3})]
        new_lines = VGroup(*self.getEdges(idx_to_node, edges))
        self.play(Transform(rvg, n_rvg), Transform(lines, new_lines))

        self.play(FadeOut(step1))
    
        step2 = Text('2. Add fake edges to make a complete graph.', font_size=30).align_on_border(DOWN)
        self.play(Create(step2))
        fake_edges = [(0, 'FAKE_NODE_1', {'weight': 0}), (0, 'FAKE_NODE_0', {'weight': 0}), (0, 6, {'weight': 0}), (1, 'FAKE_NODE_1', {'weight': 0}), (1, 'FAKE_NODE_0', {'weight': 0}), (1, 7, {'weight': 0}), (2, 'FAKE_NODE_1', {'weight': 0}), (2, 'FAKE_NODE_0', {'weight': 0}), (2, 5, {'weight': 0}), (3, 'FAKE_NODE_1', {'weight': 0}), (3, 'FAKE_NODE_0', {'weight': 0}), (3, 7, {'weight': 0}), (4, 'FAKE_NODE_1', {'weight': 0}), (4, 'FAKE_NODE_0', {'weight': 0})]
        # fake_lines = new_lines.copy()
        fake_lines = VGroup(*self.getEdges(idx_to_node, fake_edges))
        self.play(FadeIn(fake_lines))
        
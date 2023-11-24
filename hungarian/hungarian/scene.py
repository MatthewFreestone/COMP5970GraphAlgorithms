from manim import *
from collections import defaultdict

class Bipartite2(Scene):
    def createGraphVDict(self, edges, left_node_constructor = None, right_node_constructor = None):
        if not left_node_constructor:
            left_node_constructor = lambda : Circle(fill_opacity=0.8, color='RED').scale(0.3)
        if not right_node_constructor:
            right_node_constructor = lambda : Circle(fill_opacity=0.8, color='BLUE').scale(0.3)

        left_nodes = VDict(show_keys=False)
        right_nodes = VDict(show_keys=False)
        for u,v, _ in edges:
            if u not in left_nodes:
                left_nodes[u] = left_node_constructor()
            if v not in right_nodes:
                right_nodes[v] = right_node_constructor()
        return left_nodes, right_nodes

    def createGraphEdges(self, edges, left_nodes, right_nodes,  label_constructor = None, line_constructor = None):
        if not label_constructor:
            label_constructor = lambda d: Text(str(d['weight']), font_size=24)
        if not line_constructor:
            def line_constructor(label, node1, node2):
                return LabeledLine(label=label, start=node1, end=node2, label_position=0.2, label_frame=False)
        lines = defaultdict(VDict)
        for u,v,d in edges:
            lines[u][v] = line_constructor(label_constructor(d), left_nodes[u], right_nodes[v])
        return lines
    
    def updateNodes(self, edges, old_right, right_node_constructor = None):
        if not right_node_constructor:
            right_node_constructor = lambda : Circle(fill_opacity=0.3, color='BLUE').scale(0.3)
        new_r = old_right.copy()
        for u,v, _ in edges:
            if v not in new_r:
                new_r[v] = right_node_constructor()
        return new_r
    
    def augment(self, augmenting_path, lines):
        # augmenting path starts on left, terminates somewhere on the right
        used_lines = []
        result = []
        green = []
        for i in range(len(augmenting_path)):
            if i % 2 == 0:
                u,v = augmenting_path[i], augmenting_path[i+1]
                l = lines[u][v]
                used_lines.append((u,v))
                gl = l.copy()
                gl.stroke_color = ManimColor('#00FF00')
                green.append(Transform(l, gl))

                nl = l.copy()
                nl.stroke_color = ManimColor('#FF0000')
                result.append(Transform(l, nl))
            else:
                if i == len(augmenting_path) - 1:
                    continue
                u,v = augmenting_path[i], augmenting_path[i+1]
                l = lines[v][u]
                used_lines.append((v,u))
                gl = l.copy()
                gl.stroke_color = ManimColor('#00FF00')
                green.append(Transform(l, gl))

                nl = l.copy()
                nl.stroke_color = ManimColor('#000000')
                result.append(Transform(l, nl))
        # consider https://docs.manim.community/en/stable/reference/manim.animation.movement.MoveAlongPath.html#manim.animation.movement.MoveAlongPath 
        self.play(Succession(*green))
        self.play(*result)
        return used_lines
    
    def failedAugment(self, partial_path, lines, left_nodes, right_nodes):
        # failed augmenting path starts on left, terminates somewhere not on left unmatched
                
        path = []
        cutset_nodes = [left_nodes[partial_path[0]]]
        for i in range(len(partial_path)):
            if i == len(partial_path) - 1:
                continue
            u,v = partial_path[i], partial_path[i+1]
            cutset_nodes.append(left_nodes.submob_dict.get(v, None) or right_nodes.submob_dict.get(v,None))
            
            l = lines[u][v] if i % 2 == 0 else lines[v][u]
            nl = l.copy()
            nl.stroke_color = ManimColor('#00FF00')
            path.append(Transform(l, nl))
        # consider https://docs.manim.community/en/stable/reference/manim.animation.movement.MoveAlongPath.html#manim.animation.movement.MoveAlongPath 
        self.play(Succession(*path))

        cutset_transform = []
        for c in cutset_nodes:
            nc = c.copy()
            nc.stroke_color = ManimColor('#00FF00')
            cutset_transform.append(Transform(c,nc))
        self.play(*cutset_transform)
        self.play(Indicate(cutset_nodes[-1]))

    def drawAcrossCutset(self, all_lines, across):
        to_fade_in = []
        for u, outs in all_lines.items():
            for v in outs.submob_dict.keys():
                if (u,v) in across:
                    to_fade_in.append(outs[v])
        self.play(*map(FadeIn, to_fade_in))
        return to_fade_in

    def adjustPotentials(self, new_potentials, potentials_vdict, right_node, left_nodes):
        new_potentials_vdict = potentials_vdict.copy()
        potentials_transform = []
        for k,v in new_potentials.items():
            old = new_potentials_vdict[k]
            if old.text != str(v):
                new_potentials_vdict[k] = Text(str(v), font_size=old.font_size).align_to(old, UP).align_to(old,LEFT)
                potentials_transform.append(Transform(potentials_vdict[k], new_potentials_vdict[k]))
        self.play(*potentials_transform)

        node_transforms = []
        # copy_left = left_nodes.copy()
        for k,v in left_nodes.submob_dict.items():
            if v.stroke_color != ManimColor('#fc6255'):
                new_node = v.copy()
                new_node.stroke_color = '#fc6255'
                node_transforms.append(Transform(v, new_node))

        # copy_left = left_nodes.copy()
        for k,v in right_node.submob_dict.items():
            if v.stroke_color != ManimColor('#58c4dd'):
                new_node = v.copy()
                new_node.stroke_color = '#58c4dd'
                node_transforms.append(Transform(v, new_node))
        self.play(*node_transforms)


    def showOnlyMatched(self, all_lines:dict[int, VDict], visible: set, matched_lines:set):
        to_fade_out = []
        others = []
        for u, outs in all_lines.items():
            for v in outs.submob_dict.keys():
                if (u,v) in visible:
                    if (u,v) not in matched_lines:
                        to_fade_out.append(outs[v])
                    else:
                        others.append(outs[v])
        back_to_red = []
        for l in others:
            if l.stroke_color != ManimColor('#FF0000'):
                nl = l.copy()
                nl.stroke_color = ManimColor('#FF0000')
                back_to_red.append(Transform(l, nl))
        self.play(*map(FadeOut, to_fade_out), *back_to_red)



    def construct(self):
        BUFF = 0.7
        OFFSET = 4
        edges = [(0, 5, {'weight': 3}), (0, 7, {'weight': 1}), (1, 5, {'weight': 4}), (1, 6, {'weight': 8}), (2, 6, {'weight': 1}), (2, 7, {'weight': 3}), (3, 5, {'weight': 6}), (3, 6, {'weight': 2}), (4, 5, {'weight': 5}), (4, 6, {'weight': 6}), (4, 7, {'weight': 3})]
        l,original_r = self.createGraphVDict(edges)
        l.arrange(UP, buff=BUFF).shift(OFFSET * LEFT)
        original_r.arrange(UP, buff=BUFF).shift(OFFSET * RIGHT)
        lines = self.createGraphEdges(edges, l, original_r)

        self.add(Text('Maximum Weighted Bipartite Matching', font_size=36).align_on_border(UP))
        self.play(Create(l))
        self.play(Create(original_r))
        self.play(*map(FadeIn, lines.values()))

        fake_edges = [(0, 'F_1', {'weight': 0}), (0, 6, {'weight': 0}), (0, 'F_0', {'weight': 0}), (1, 'F_1', {'weight': 0}), (1, 7, {'weight': 0}), (1, 'F_0', {'weight': 0}), (2, 'F_1', {'weight': 0}), (2, 5, {'weight': 0}), (2, 'F_0', {'weight': 0}), (3, 'F_1', {'weight': 0}), (3, 7, {'weight': 0}), (3, 'F_0', {'weight': 0}), (4, 'F_1', {'weight': 0}), (4, 'F_0', {'weight': 0})]
        r = self.updateNodes(fake_edges, original_r)
        r.arrange(UP, buff=BUFF).shift(OFFSET * RIGHT)
        # self.play(Transform(original_r, r))
        
        all_lines = self.createGraphEdges(edges, l, r)

        def dottedline_constructor(label, node1, node2):
                return DashedLine(start=node1, end=node2)
        fake_lines = self.createGraphEdges(fake_edges, l, r, line_constructor=dottedline_constructor)

        transform_line_pairs = ((lines[x], all_lines[x]) for x in lines.keys())
        transform_right_pairs = [(original_r[x], r[x]) for x in original_r.submob_dict.keys()]
        fade_in_right = [r[x] for x in r.submob_dict.keys() if x not in original_r]
        step1 = Text('1. Add fake nodes to allow perfect matching.', font_size=30).align_on_border(DOWN)
        self.play(Create(step1))
        # self.play(Transform(original_r, r), *map(lambda x: Transform(x[0],x[1]), transform_line_pairs))
        transform = lambda x: Transform(x[0],x[1])
        self.play(*map(transform, transform_right_pairs), *map(transform, transform_line_pairs))
        self.play(*map(FadeIn, fade_in_right))
        self.play(FadeOut(step1))
        self.remove(*lines.values())
        # self.remove(r)
        self.add(*all_lines.values())
        # self.add(r)

        
        self.wait()
        
        step2 = Text('2. Add fake edges (with weight < min(edge weight)) to make a complete graph.', font_size=24).align_on_border(DOWN)
        self.play(Create(step2))
        self.play(*map(FadeIn, fake_lines.values()))

        for k,v in fake_lines.items():
            # v is VDict
            for dest in v.submob_dict.keys():
                all_lines[k][dest] = v[dest]

        # print(all_lines)
        self.remove(*fake_lines.values())
        self.add(*all_lines.values())
        # self.remove(*all_lines.values())

        self.wait()

        self.play(FadeOut(step2))
        step3 = Text('3. Assign potentials to left side based on max outgoing weight.', font_size=30).align_on_border(DOWN)
        self.play(Create(step3))

        potentials = {0: 3, 1: 8, 2: 3, 3: 6, 4: 6, 5: 0, 6: 0, 7: 0, 'F_1': 0, 'F_0': 0}
        potentials_vdict = VDict()
        for k, v in potentials.items():
            label = Text(str(v), font_size=24)
            if k in l:
                label.next_to(l[k], LEFT)
            else:
                label.next_to(r[k], RIGHT)
            potentials_vdict[k] = label

        self.play(FadeIn(potentials_vdict))

        self.wait()

        self.play(FadeOut(step3))


        step4a = Tex('4a. Only show edges s.t. $l(x) + l(y) = w(e)$', font_size=36).align_on_border(DOWN)
        self.play(Create(step4a))

        visible =  {(0, 5), (1, 6), (2, 7), (3, 5), (4, 6)}
        to_fade_out = []
        for u, outs in all_lines.items():
            for v in outs.submob_dict.keys():
                if (u,v) not in visible:
                    to_fade_out.append(outs[v])
        self.play(*map(FadeOut,to_fade_out))
        self.wait()


        self.play(FadeOut(step4a))

        step4b = Text('4b. Run Standard Augmenting Path Algorithm', font_size=24).align_on_border(DOWN)
        self.play(Create(step4b))

        matched_lines = []
        matched_lines.extend(self.augment([0,5], all_lines))
        matched_lines.extend(self.augment([1,6], all_lines))
        matched_lines.extend(self.augment([2,7], all_lines))

        self.failedAugment([3,5,0], all_lines, l, r)
        step4b2 = Text('4b. Augmenting Path Stuck, but not all nodes matched', font_size=24).align_on_border(DOWN)
        
        self.play(Succession(FadeOut(step4b),FadeIn(step4b2)))
        step4c = Text('4c. Adjust potentials across visited nodes and unvisited.', font_size=24).align_on_border(DOWN)
        self.play(Succession(FadeOut(step4b2), FadeIn(step4c)))



        self.showOnlyMatched(all_lines, visible, matched_lines)

        across = {(0, 7): 2, (0, 'F_0'): 3, (0, 6): 3, (0, 'F_1'): 3, (3, 6): 4, (3, 'F_0'): 6, (3, 7): 6, (3, 'F_1'): 6}
        to_fade_out = self.drawAcrossCutset(all_lines, across)

        step4c2 = Tex('$$\\textrm{4c. change} = \min_{x \in S, y \in T}(l(x)+l(y)-w(x,y))$$', font_size=36).align_on_border(DOWN)
        self.play(Succession(FadeOut(step4c), FadeIn(step4c2)))
        self.wait()
        caption = Tex(f"$= \min({','.join(map(str, across.values()))}) = {min(across.values())}$", font_size=36).align_on_border(DOWN)
        self.play(Succession(FadeOut(step4c2), FadeIn(caption)))
        self.wait()

        new_potentials = {0: 1, 1: 8, 2: 3, 3: 4, 4: 6, 5: 2, 6: 0, 7: 0, 'F_0': 0, 'F_1': 0}
        self.adjustPotentials(new_potentials, potentials_vdict, r, l)

        self.play(*map(FadeOut, to_fade_out))
        self.play(FadeOut(caption))


        ######### NEXT ITERATION ########

        self.play(Create(step4a))
        visible =  {(0, 7), (2, 7), (4, 6), (0, 5), (1, 6), (3, 5)}
        to_fade_in = []
        for u, outs in all_lines.items():
            for v in outs.submob_dict.keys():
                if (u,v) in visible:
                    if outs[v].stroke_color != ManimColor("#FF0000"):
                        outs[v].stroke_color = ManimColor("#FFFFFF")
                        to_fade_in.append(outs[v])
        self.play(*map(FadeIn,to_fade_in))
        self.wait()


        self.play(FadeOut(step4a))

        step4b = Text('4b. Run Standard Augmenting Path Algorithm', font_size=24).align_on_border(DOWN)
        self.play(Create(step4b))

        self.failedAugment([3, 5, 0, 7, 2], all_lines, l, r)
        step4b2 = Text('4b. Augmenting Path Stuck, but not all nodes matched', font_size=24).align_on_border(DOWN)
        
        # self.play(Succession(FadeOut(step4b),FadeIn(step4b2)))
        # step4c = Text('4c. Adjust potentials across visited nodes and unvisited.', font_size=24).align_on_border(DOWN)
        # self.play(Succession(FadeOut(step4b2), FadeIn(step4c)))



        # self.showOnlyMatched(all_lines, visible, matched_lines)

        # across = {(0, 7): 2, (0, 'F_0'): 3, (0, 6): 3, (0, 'F_1'): 3, (3, 6): 4, (3, 'F_0'): 6, (3, 7): 6, (3, 'F_1'): 6}
        # to_fade_out = self.drawAcrossCutset(all_lines, across)

        # step4c2 = Tex('$$\\textrm{4c. change} = \min_{x \in S, y \in T}(l(x)+l(y)-w(x,y))$$', font_size=36).align_on_border(DOWN)
        # self.play(Succession(FadeOut(step4c), FadeIn(step4c2)))
        # self.wait()
        # caption = Tex(f"$= \min({','.join(map(str, across.values()))}) = {min(across.values())}$", font_size=36).align_on_border(DOWN)
        # self.play(Succession(FadeOut(step4c2), FadeIn(caption)))
        # self.wait()

        # new_potentials = {0: 1, 1: 8, 2: 3, 3: 4, 4: 6, 5: 2, 6: 0, 7: 0, 'F_0': 0, 'F_1': 0}
        # self.adjustPotentials(new_potentials, potentials_vdict)

        # self.play(*map(FadeOut, to_fade_out))



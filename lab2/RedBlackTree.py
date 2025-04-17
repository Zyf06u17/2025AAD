from graphviz import Digraph
import os
import msvcrt
import random
random.seed(38)
import time 

class Node:
    def __init__(self, val, color='red'):
        self.val = val  # 节点的值
        self.color = color  # 节点的颜色（红色或黑色）
        self.left = None  # 左子节点
        self.right = None  # 右子节点
        self.parent = None  # 父节点

class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None, 'black')  # 哨兵节点，表示空节点
        self.root = self.NIL  # 初始化根节点为哨兵节点

    # 插入新值到红黑树
    def insert(self, val):
        new_node = Node(val, 'red')  # 新插入的节点默认为红色
        new_node.left = self.NIL  # 左子节点初始化为哨兵节点
        new_node.right = self.NIL  # 右子节点初始化为哨兵节点
        self._insert_node(new_node)  # 插入节点到树中
        self._fix_insert(new_node)  # 修复红黑树性质

    # 插入节点到树中
    def _insert_node(self, new_node):
        parent = None
        current = self.root

        # 找到插入位置
        while current != self.NIL:
            parent = current
            if new_node.val < current.val:
                current = current.left
            else:
                current = current.right

        # 设置新节点的父节点
        new_node.parent = parent
        if parent is None:
            self.root = new_node  # 如果父节点为空，新节点为根节点
        elif new_node.val < parent.val:
            parent.left = new_node  # 插入到父节点的左子树
        else:
            parent.right = new_node  # 插入到父节点的右子树

    # 修复红黑树性质
    def _fix_insert(self, node):
        while node != self.root and node.parent.color == 'red':  # 父节点为红色时需要修复
            if node.parent == node.parent.parent.left:  # 父节点是祖父节点的左子节点
                uncle = node.parent.parent.right  # 获取叔叔节点
                if uncle.color == 'red':  # 情况 1：叔叔节点为红色
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:  # 情况 2：当前节点是父节点的右子节点
                        node = node.parent
                        self._rotate_left(node)  # 左旋父节点
                    # 情况 3：当前节点是父节点的左子节点
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self._rotate_right(node.parent.parent)  # 右旋祖父节点
            else:  # 父节点是祖父节点的右子节点，类似的对称情况
                uncle = node.parent.parent.left  # 获取叔叔节点
                if uncle.color == 'red':  # 情况 1：叔叔节点为红色
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:  # 情况 2：当前节点是父节点的左子节点
                        node = node.parent
                        self._rotate_right(node)  # 右旋父节点
                    # 情况 3：当前节点是父节点的右子节点
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self._rotate_left(node.parent.parent)  # 左旋祖父节点
        self.root.color = 'black'  # 确保根节点为黑色

    # 删除节点
    def delete(self, val):
        node = self.find(val)  # 查找要删除的节点
        if node:
            self._delete_node(node)  # 删除节点

    # 删除节点的具体实现
    def _delete_node(self, node):
        y = node
        y_original_color = y.color  # 保存被删除节点的颜色

        if node.left == self.NIL:  # 
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.NIL:  # 节点只有左子树 
            x = node.left
            self._transplant(node, node.left)
        else:  # 节点有两个子树 
            y = self._minimum(node.right)  # 找到后继节点
            y_original_color = y.color#转为删除后继结点的颜色
            x = y.right

            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y

            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
            #这里直接将后继结点替换了原本待删除的结点，原来后继结点的位置被右子树顶上了
        if y_original_color == 'black':  # 如果被删除节点是黑色，需要修复红黑树性质
            self._fix_delete(x)

    # 替换子树
    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # 找到最小值节点
    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    # 修复删除后的红黑树性质
    def _fix_delete(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                w = x.parent.right  # 获取兄弟节点
                if w.color == 'red':  # 情况 1：兄弟节点为红色 转换为情况2,3,4中去解决
                    w.color = 'black'
                    x.parent.color = 'red'
                    self._rotate_left(x.parent)
                    w = x.parent.right
                if w.left.color == 'black' and w.right.color == 'black':  # 情况 2：兄弟节点的子节点都为黑色
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.right.color == 'black':  # 情况 3：兄弟节点的右子节点为黑色，转换为情况4去解决
                        w.left.color = 'black'
                        w.color = 'red'
                        self._rotate_right(w)
                        w = x.parent.right
                    # 情况 4：兄弟节点的右子节点为红色
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.right.color = 'black'
                    self._rotate_left(x.parent)
                    x = self.root
            else:  # 对称情况
                w = x.parent.left
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self._rotate_right(x.parent)
                    w = x.parent.left
                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self._rotate_left(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.left.color = 'black'
                    self._rotate_right(x.parent)
                    x = self.root
        x.color = 'black'

    # 左旋
    def _rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left != self.NIL:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    # 右旋
    def _rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right != self.NIL:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

    # 查找节点
    def find(self, val):
        return self._find_node(self.root, val)

    def _find_node(self, node, val):
        while node != self.NIL:
            if val == node.val:
                return node
            elif val < node.val:
                node = node.left
            else:
                node = node.right
        return None

    # 可视化红黑树
    def visualize_tree(self, filename="red_black_tree"):
        dot = Digraph(comment='Red Black Tree')
        dot.attr('node', shape='circle', style='filled')

        def add_nodes_edges(node):
            if node != self.NIL:
                # 设置节点颜色和字体颜色
                fillcolor = "red" if node.color == "red" else "black"
                fontcolor = "white" if node.color == "black" else "black"
                dot.node(str(id(node)), str(node.val), fillcolor=fillcolor, fontcolor=fontcolor)

                # 添加左子节点和边
                if node.left != self.NIL:
                    dot.edge(str(id(node)), str(id(node.left)), label="L")
                    add_nodes_edges(node.left)
                else:
                    # 添加左侧哨兵节点
                    nil_id = f"nil_l_{id(node)}"
                    dot.node(nil_id, "NIL", fillcolor="black", fontcolor="white", shape='square', width='0.3', height='0.3')
                    dot.edge(str(id(node)), nil_id, label="L")

                # 添加右子节点和边
                if node.right != self.NIL:
                    dot.edge(str(id(node)), str(id(node.right)), label="R")
                    add_nodes_edges(node.right)
                else:
                    # 添加右侧哨兵节点
                    nil_id = f"nil_r_{id(node)}"
                    dot.node(nil_id, "NIL", fillcolor="black", fontcolor="white", shape='square', width='0.3', height='0.3')
                    dot.edge(str(id(node)), nil_id, label="R")

        add_nodes_edges(self.root)
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        dot.render(f'{output_dir}/{filename}', view=False, format='png')


def generate_random_array(n):
    return [random.randint(0, 100000) for _ in range(n)]

# if __name__ == "__main__":
#     rbt = RedBlackTree()
#     n = 15
#     nums = generate_random_array(n)
#     print("随机生成的数组:", nums)
#     print("开始构建红黑树...")
    
#     for num in nums:
#         rbt.insert(num)
#         rbt.visualize_tree()  # 使用默认文件名
#         print(f"插入 {num} 后的红黑树已更新")
#         print("按下任意键继续...")
#         msvcrt.getch()
    
#     print("\n红黑树构建完成！请选择操作：")
#     while True:
#         print("\n1. 插入新节点")
#         print("2. 查找节点")
#         print("3. 删除节点")
#         print("4. 退出程序")
#         choice = input("请输入选择 (1/2/3/4): ")
        
#         if choice == '1':
#             val = int(input("请输入要插入的值: "))
#             rbt.insert(val)
#             rbt.visualize_tree()  # 使用默认文件名
#             print(f"已插入值 {val} 并更新可视化")
        
#         elif choice == '2':
#             val = int(input("请输入要查找的值: "))
#             result = rbt.find(val)
#             if result:
#                 print(f"找到值 {val}")
#             else:
#                 print(f"未找到值 {val}")
        
#         elif choice == '3':
#             val = int(input("请输入要删除的值: "))
#             rbt.delete(val)
#             rbt.visualize_tree()  # 使用默认文件名
#             print(f"已删除值 {val} 并更新可视化")
        
#         elif choice == '4':
#             print("程序结束")
#             break
        
#         else:
#             print("无效的选择，请重新输入")


if __name__ == "__main__":
    rbt = RedBlackTree()
    random_array = [random.randint(1, 100000) for _ in range(30000)]
    # print(random_array);
    startTime=time.perf_counter()
    for num in random_array:
        rbt.insert(num)
    endTime=time.perf_counter()
    elapsed_time_ms=(endTime-startTime)*1000        
    print(f"插入随机数组时间为：{elapsed_time_ms:.2f}毫秒")

    startTime=time.perf_counter()
    rbt.insert(8888)
    endTime=time.perf_counter()
    elapsed_time_ms=(endTime-startTime)*1000
    print(f"插入8888的时间为：{elapsed_time_ms:.2f}毫秒")
    
    startTime=time.perf_counter()
    rbt.delete(random_array[9])
    endTime=time.perf_counter()
    elapsed_time_ms=(endTime-startTime)*1000
    print(f"删除random_array[9]的时间为：{elapsed_time_ms:.2f}毫秒")
    
    startTime=time.perf_counter()
    rbt.find(11111)
    endTime=time.perf_counter()
    elapsed_time_ms=(endTime-startTime)*1000
    print(f"查找11111的时间为：{elapsed_time_ms:.2f}毫秒")
    

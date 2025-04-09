from graphviz import Digraph
import os
import msvcrt
import random
class AVLTreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1#初始高度为1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        if not node:
            return AVLTreeNode(val)
        elif val < node.val:
            node.left = self._insert(node.left, val)
        else:
            node.right = self._insert(node.right, val)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return self._balance(node)#在插入后，需要进行平衡操作

    def delete(self, val):
        self.root = self._delete(self.root, val)

    def _delete(self, node, val):
        if not node:
            return node
        elif val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._get_min_value_node(node.right)#找到右子树的最小值，也就是找到被删除结点的后继结点
            node.val = temp.val
            node.right = self._delete(node.right, temp.val)#递归删除后继结点

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return self._balance(node) #同样地，在删除后，需要进行平衡操作

    def find(self, val):
        return self._find(self.root, val)

    def _find(self, node, val):
        current = node
        while current:
            if current.val == val:
                return current
            elif val < current.val:
                current = current.left
            else:
                current = current.right
        return None

    def _get_min_value_node(self, node):#调用此函数时，是找被删除结点的后继结点，所以需要找左子树的最小值，一直向左找
        current = node
        while current.left:
            current = current.left
        return current

    def _get_height(self, node):   #计算高度
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):#计算平衡因子
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)        #左子树高度减去右子树高度

    def _balance(self, node):#平衡操作
        balance = self._get_balance(node)

        if balance > 1: 
            if self._get_balance(node.left) < 0:#获取左子树的平衡因子，如果小于0，说明是LR型，先左孩子左旋，再根节点右旋
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)#LL型，直接右旋

        if balance < -1:
            if self._get_balance(node.right) > 0:#获取右子树的平衡因子，如果大于0，说明是RL型，先右孩子右旋，再根节点左旋
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)#RR型，直接左旋

        return node

    def _rotate_left(self, z): #左旋(z为根节点)
        y = z.right #建立一个指针y指向z的右孩子
        T2 = y.left #建立一个指针T2指向y的左孩子
        y.left = z #y的左孩子指向z
        z.right = T2 #z的右孩子指向T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y
        
    def _rotate_right(self, z):#右旋(z为根节点) 
        y = z.left #建立一个指针y指向z的左孩子       
        T3 = y.right #建立一个指针T3指向y的右孩子
        y.right = z #y的右孩子指向z
        z.left = T3 #z的左孩子指向T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def visualize_tree(self, filename="tree"):#可视化树
        dot = Digraph(comment='AVL Tree')
        dot.attr('node', shape='circle')

        def add_nodes_edges(node):
            if node:
                dot.node(str(id(node)), str(node.val))
                if node.left:
                    dot.edge(str(id(node)), str(id(node.left)), label="L")
                    add_nodes_edges(node.left)
                if node.right:
                    dot.edge(str(id(node)), str(id(node.right)), label="R")
                    add_nodes_edges(node.right)

        add_nodes_edges(self.root)
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        dot.render(f'{output_dir}/{filename}', view=False, format='png')

def generate_random_array(n):
    return [random.randint(0, 100000) for _ in range(n)]

if __name__ == "__main__":
    avl = AVLTree()
    n = 30
    nums = generate_random_array(n)
    print(nums)
    print("随机的数组构建完毕")
    for num in nums:
        avl.insert(num)
        avl.visualize_tree(filename="AVL_tree")
        # print("按下任意键继续...")
        # msvcrt.getch()
        # print("当前插入已经完成，程序继续执行。")
    print("AVL树已经构建完成，选择你要执行的操作：")
    while True:
        print("1. 插入")
        print("2. 查找")
        print("3. 删除")
        print("4. 退出")
        choice = input("请输入你的选择 (1/2/3/4): ")
        if choice == '1':
            val = int(input("请输入要插入的值: "))
            avl.insert(val)
            avl.visualize_tree(filename="AVL_tree")
            print(f"{val} 已插入到AVL树中。")
        elif choice == '2':
            val = int(input("请输入要查找的值: "))
            result = avl.find(val)
            if result:
                print(f"找到了值 {val}。")
            else:
                print(f"未找到值 {val}。")
        elif choice == '3':
            val = int(input("请输入要删除的值: "))
            avl.delete(val)
            avl.visualize_tree(filename="AVL_tree")
            print(f"{val} 已从AVL树中删除。")
        elif choice == '4':
            print("退出程序。")
            break
        else:
            print("无效的选择，请重新输入。")
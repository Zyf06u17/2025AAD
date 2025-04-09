from graphviz import Digraph
import os
import msvcrt
import random
##树的结点
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
class BST:#一个 类的封装，方便后续调用
    def __init__(self):
        self.root = None

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, root, val): #递归操作，递归结束就是要插入的地方
        if root is None:
            return TreeNode(val)
        if val < root.val:#小于当前，向左子树插
            root.left = self._insert(root.left, val)
        else:
            root.right = self._insert(root.right, val)
        return root

    def delete(self, val):
        self.root = self._delete(self.root, val)

    def _delete(self, root, val):
        if root is None:
            return root
        if val < root.val:#根据当前结点与待删val比较，如果大了就去左子树找，如果正是此结点应该被删
            root.left = self._delete(root.left, val)
        elif val > root.val:
            root.right = self._delete(root.right, val)
        else:#分三种情况
            if root.left is None:#子树只有左子树
                return root.right
            elif root.right is None:#
                return root.left
            temp = self._find_min(root.right)#左右子树都存在，找后继结点
            root.val = temp.val#赋予
            root.right = self._delete(root.right, temp.val)#再删后继
        return root

    def find(self, val):
        return self._find(self.root, val)

    def _find(self, root, val):#顺着大小找
        current = root
        while current:
            if current.val == val:
                return current
            elif val < current.val:
                current = current.left
            else:
                current = current.right
        return None

    def _find_min(self, node):#这里是方便delete找后继
        current = node
        while current.left:
            current = current.left
        return current

    def visualize_tree(self, filename="tree"):#可视化操作，方便我们看到树的结构
        dot = Digraph(comment='Binary Tree')
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
    bst = BST()
    n = 30
    nums = generate_random_array(n)
    print(nums)
    print("随机的数组构建完毕")
    for num in nums:
        bst.insert(num)
        bst.visualize_tree(filename="BST_tree")
        print("按下任意键继续...")
        msvcrt.getch()
        print("当前插入已经完成，程序继续执行。")
    print("二叉搜索树已经构建完成，选择你要执行的操作：")
    while True:
        print("1. 插入")
        print("2. 查找")
        print("3. 删除")
        print("4. 退出")
        choice = input("请输入你的选择 (1/2/3/4): ")
        if choice == '1':
            val = int(input("请输入要插入的值: "))
            bst.insert(val)
            bst.visualize_tree(filename="BST_tree")
            print(f"{val} 已插入到二叉搜索树中。")
        elif choice == '2':
            val = int(input("请输入要查找的值: "))
            result = bst.find(val)
            if result:
                print(f"找到了值 {val}。")
            else:
                print(f"未找到值 {val}。")
        elif choice == '3':
            val = int(input("请输入要删除的值: "))
            bst.delete(val)
            bst.visualize_tree(filename="BST_tree")
            print(f"{val} 已从二叉搜索树中删除。")
        elif choice == '4':
            print("退出程序。")
            break
        else:
            print("无效的选择，请重新输入。")
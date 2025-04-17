from graphviz import Digraph
import os
import msvcrt
import random
import time     
random.seed(38)#设立随机种子，在其他树代码中也设置相同的，确保我们用的随机数一致

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
        if self.root is None:
            self.root = TreeNode(val)
            return
        
        current = self.root
        while True:
            if val < current.val:
                if current.left is None:
                    current.left = TreeNode(val)
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = TreeNode(val)
                    break
                current = current.right

    def delete(self, val):
        if self.root is None:
            return

        # 找到要删除的节点及其父节点
        parent = None
        current = self.root
        while current and current.val != val:
            parent = current
            if val < current.val:
                current = current.left
            else:
                current = current.right

        if current is None:  # 没找到要删除的节点
            return

        # 情况1：要删除的节点有两个子节点
        if current.left and current.right:
            # 找到右子树的最小节点
            successor_parent = current
            successor = current.right
            while successor.left:
                successor_parent = successor
                successor = successor.left

            # 用后继节点的值替换当前节点的值
            current.val = successor.val
            # 删除后继节点（后继节点最多只有一个右子节点）
            if successor_parent.left == successor:
                successor_parent.left = successor.right
            else:
                successor_parent.right = successor.right

        # 情况2：要删除的节点是叶子节点或只有一个子节点
        else:
            # 确定要替换当前节点的子节点
            child = current.left if current.left else current.right

            # 更新父节点的引用
            if parent is None:  # 删除的是根节点
                self.root = child
            elif parent.left == current:
                parent.left = child
            else:
                parent.right = child

    def find(self, val):
        current = self.root
        while current:
            if current.val == val:
                return current
            elif val < current.val:
                current = current.left
            else:
                current = current.right
        return None

    def _find_min(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def visualize_tree(self, filename="tree"):
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

# if __name__ == "__main__":
#     bst = BST()
#     n = 15
#     nums = generate_random_array(n)
#     print(nums)
#     print("随机的数组构建完毕")
#     for num in nums:
#         bst.insert(num)
#         bst.visualize_tree(filename="BST_tree")
#         # print("按下任意键继续...")
#         # msvcrt.getch()
#         # print("当前插入已经完成，程序继续执行。")


#     print("二叉搜索树已经构建完成，选择你要执行的操作：")
#     while True:
#         print("1. 插入")
#         print("2. 查找")
#         print("3. 删除")
#         print("4. 退出")
#         choice = input("请输入你的选择 (1/2/3/4): ")
#         if choice == '1':
#             val = int(input("请输入要插入的值: "))
#             bst.insert(val)
#             bst.visualize_tree(filename="BST_tree")
#             print(f"{val} 已插入到二叉搜索树中。")
#         elif choice == '2':
#             val = int(input("请输入要查找的值: "))
#             result = bst.find(val)
#             if result:
#                 print(f"找到了值 {val}。")
#             else:
#                 print(f"未找到值 {val}。")
#         elif choice == '3':
#             val = int(input("请输入要删除的值: "))
#             bst.delete(val)
#             bst.visualize_tree(filename="BST_tree")
#             print(f"{val} 已从二叉搜索树中删除。")
#         elif choice == '4':
#             print("退出程序。")
#             break
#         else:
#             print("无效的选择，请重新输入。")

if __name__ == "__main__":
    bst = BST()
    random_array = [random.randint(1, 100000) for _ in range(30000)]
    # print(random_array);
    startTime=time.perf_counter()
    for num in random_array:
        bst.insert(num)
    endTime=time.perf_counter();
    elapsed_time_ms=(endTime-startTime)*1000        
    print(f"插入随机数组时间为：{elapsed_time_ms:.2f}毫秒")

    startTime=time.perf_counter()
    bst.insert(8888)
    endTime=time.perf_counter()
    elapsed_time_ms=(endTime-startTime)*1000
    print(f"插入8888的时间为：{elapsed_time_ms:.2f}毫秒")

    startTime=time.perf_counter()
    bst.delete(random_array[9])
    endTime=time.perf_counter()
    elapsed_time_ms=(endTime-startTime)*1000
    print(f"删除random_array[9]的时间为：{elapsed_time_ms:.2f}毫秒")
    
    startTime=time.perf_counter()
    bst.find(11111)
    endTime=time.perf_counter()
    elapsed_time_ms=(endTime-startTime)*1000
    print(f"查找11111的时间为：{elapsed_time_ms:.2f}毫秒")
    
    
    
    

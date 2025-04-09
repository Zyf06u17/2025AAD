from random import shuffle
import random

root_node = None

# B 树的阶数
_M = 5


class Logger(object):
    """
    用于打印 B 树结构的日志工具类
    """
    @classmethod
    def tree(cls, node, child_name, dsc, depth):
        """
        递归打印树的结构
        :param node: 当前节点
        :param child_name: 子节点属性名
        :param dsc: 描述函数，用于格式化节点内容
        :param depth: 当前深度
        """
        if depth == 0:
            head = "|   " * depth
            print(head + "+--" + dsc(node))
            depth = depth + 1

        for child in getattr(node, child_name):
            head = "|   " * depth
            print(head + "+--" + dsc(child))
            cls.tree(child, child_name, dsc, depth + 1)


class BKeyword(object):
    def __init__(self, key):
        self.key = key 


class BNode(object):
    def __init__(self):
        self._parent: BNode = None  # 父节点
        self.keywords = []  # 当前节点的关键字列表
        self.child_nodes = []  # 当前节点的子节点列表

    def set_parent(self, node):
        self._parent = node
        if node.get_parent() is None:
            global root_node
            root_node = node.get_parent()

    def get_parent(self):
        return self._parent

    def insert_child_node(self, index, add_node):
        add_node.set_parent(self)
        self.child_nodes.insert(index, add_node)

    def append_child_node(self, add_node):
        add_node.set_parent(self)
        self.child_nodes.append(add_node)

    def find_add_index(self, add_word):
        if len(self.keywords) == 0:
            return 0
        index = 0
        while True:
            if index >= len(self.keywords):
                break
            key = self.keywords[index].key
            if add_word.key < key:
                break
            index = index + 1
        return index

    def blind_add(self, word: BKeyword) -> int: #盲插，不管节点是否满   
        index = self.find_add_index(word)
        self.keywords.insert(index, word)

    def split(self):#分裂
        parent, center_keyword, left_node, right_node = self.split_to_piece()
        parent_add_index = parent.find_add_index(center_keyword)
        parent.insert_child_node(parent_add_index, right_node)
        parent.insert_child_node(parent_add_index, left_node)
        if self in parent.child_nodes:
            parent.child_nodes.remove(self)
        parent.add_word(center_keyword, force=True)
        root = self
        while root.get_parent() is not None:
            root = root.get_parent()
        global root_node
        root_node = root

    def split_to_piece(self):
       # 将当前节点分裂为三个部分：左节点、右节点和中间关键字
        center_keyword = self.keywords[int((_M-1)/2)]
        if self.get_parent() is None:
            self.set_parent(BNode())
        left_node = BNode()
        right_node = BNode()
        for keyword in self.keywords:
            if keyword.key < center_keyword.key:
                left_node.keywords.append(keyword)
            elif keyword.key > center_keyword.key:
                right_node.keywords.append(keyword)
        for i in range(len(self.child_nodes)):
            if i <= int((len(self.child_nodes) - 1)/2):
                left_node.append_child_node(self.child_nodes[i])
            else:
                right_node.append_child_node(self.child_nodes[i])
        return self.get_parent(), center_keyword, left_node, right_node

    def add_word(self, keyword, force=False):
        if len(self.child_nodes) == 0 or force:
            self.blind_add(keyword)
            if len(self.keywords) == _M:
                print("新增:" + str(keyword.key) + ", 达到阶数，分裂")
                self.split()
        else:
            index = self.find_add_index(keyword)
            if index >= len(self.child_nodes):
                index = index - 1
            self.child_nodes[index].add_word(keyword)

    def delete_word(self, key):

        # 查找关键字在当前节点中的位置
        for i, keyword in enumerate(self.keywords):
            if keyword.key == key:
                # 如果是叶子节点，直接删除关键字
                if len(self.child_nodes) == 0:
                    del self.keywords[i]
                    print(f"删除关键字: {key}")
                    return True
                else:
                    # 如果是内部节点，用后继关键字替换并递归删除后继关键字
                    successor = self.get_successor(i)
                    self.keywords[i] = successor
                    self.child_nodes[i + 1].delete_word(successor.key)
                    self.fix_child(i + 1)
                    return True

        # 如果关键字不在当前节点，递归到子节点中删除
        for i, keyword in enumerate(self.keywords):
            if key < keyword.key:
                if self.child_nodes:
                    if self.child_nodes[i].delete_word(key):
                        self.fix_child(i)
                        return True
                break

        # 如果关键字大于所有关键字，递归到最后一个子节点
        if self.child_nodes:
            if self.child_nodes[-1].delete_word(key):
                self.fix_child(len(self.child_nodes) - 1)
                return True

        # 如果关键字未找到，返回 False
        return False

    def get_successor(self, index):
        #获取后继关键字（右子树的最小关键字）
        current = self.child_nodes[index + 1]
        while current.child_nodes:
            current = current.child_nodes[0]
        return current.keywords[0]

    def fix_child(self, index):#修复子节点
        child = self.child_nodes[index]

        # 如果子节点的关键字数少于最低限制
        if len(child.keywords) < (_M // 2):
            # 尝试从左兄弟借关键字
            if index > 0 and len(self.child_nodes[index - 1].keywords) > (_M // 2):
                left_sibling = self.child_nodes[index - 1]
                child.keywords.insert(0, self.keywords[index - 1])
                self.keywords[index - 1] = left_sibling.keywords.pop()
                if left_sibling.child_nodes:
                    child.child_nodes.insert(0, left_sibling.child_nodes.pop())
            # 尝试从右兄弟借关键字
            elif index < len(self.child_nodes) - 1 and len(self.child_nodes[index + 1].keywords) > (_M // 2):
                right_sibling = self.child_nodes[index + 1]
                child.keywords.append(self.keywords[index])
                self.keywords[index] = right_sibling.keywords.pop(0)
                if right_sibling.child_nodes:
                    child.child_nodes.append(right_sibling.child_nodes.pop(0))
            # 如果无法借关键字，合并节点
            else:
                if index > 0:
                    left_sibling = self.child_nodes[index - 1]
                    left_sibling.keywords.append(self.keywords.pop(index - 1))
                    left_sibling.keywords.extend(child.keywords)
                    left_sibling.child_nodes.extend(child.child_nodes)
                    self.child_nodes.pop(index)
                else:
                    right_sibling = self.child_nodes[index + 1]
                    child.keywords.append(self.keywords.pop(index))
                    child.keywords.extend(right_sibling.keywords)
                    child.child_nodes.extend(right_sibling.child_nodes)
                    self.child_nodes.pop(index + 1)

        # 如果根节点为空且有子节点，将子节点提升为新的根节点
        global root_node
        if self == root_node and len(self.keywords) == 0:
            if len(self.child_nodes) == 1:
                root_node = self.child_nodes[0]
                root_node._parent = None
            elif len(self.child_nodes) == 0:
                root_node = None

    def search_word(self, key):
        for keyword in self.keywords:
            if keyword.key == key:
                print(f"找到关键字: {key}")
                return True
        for child in self.child_nodes:
            if child.search_word(key):
                return True
        return False


def print_tree(node):
    """
    打印 B 树的结构
    """
    print("\n******************************")

    def dsc(node):
        s = ''
        for keyword in node.keywords:
            s = s + str(keyword.key) + ','
        s = s[:-1]
        return s
    Logger.tree(node, 'child_nodes', dsc,  0)
    print("******************************")


def prepare():
    """
    准备随机数数组，用于测试
    """
    array = []
    number = 0
    for i in range(15):
        number = number + random.randint(1, 4)
        array.append(number)
    shuffle(array)
    return array


if __name__ == '__main__':
    """
    主程序入口，提供插入、删除、查找和退出功能
    """
    root_node = BNode()
    # array = prepare()
    # for i in array:
    #     keyword = BKeyword(i)  
    #     root_node.add_word(keyword)
    # print_tree(root_node)

    while True:
        print("\n请选择操作:")
        print("1. 插入值")
        print("2. 删除值")
        print("3. 查找值")
        print("4. 退出")
        choice = input("请输入你的选择 (1/2/3/4): ")

        if choice == '1':
            key = int(input("请输入要插入的值: "))
            root_node.add_word(BKeyword(key))  # 不再需要传入数据
            print_tree(root_node)
        elif choice == '2':
            key = int(input("请输入要删除的值: "))
            if not root_node.delete_word(key):
                print(f"值 {key} 不存在")
            print_tree(root_node)
        elif choice == '3':
            key = int(input("请输入要查找的值: "))
            if not root_node.search_word(key):
                print(f"值 {key} 不存在")
        elif choice == '4':
            print("程序已退出。")
            break
        else:
            print("无效选项，请重新输入")
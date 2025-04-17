if __name__ == "__main__":
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

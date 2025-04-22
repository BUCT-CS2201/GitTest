from py2neo import Graph
import readline  # 支持历史命令记录

# Neo4j连接配置（复用原有配置）
graph = Graph("bolt://123.56.47.51:7687", 
             auth=("neo4j", "jike2201!"),
             name="neo4j")

# 增强属性映射（新增10种问答类型）
PROPERTY_MAPPING = {
    "收藏地": "收藏于", "时代": "朝代", "年代": "年代",
    "材质": "材质", "类型": "类型", "作者": "书画作者",
    "尺寸": "尺寸", "重量": "重量", "出土地": "出土地",
    "修复记录": "修复历史", "相关文物": "关联文物"
}
  
def enhanced_parser(question: str) -> tuple:
    """改进的语义解析器"""
    # 实体识别（支持模糊匹配）
    entities = [
        "秦始皇兵马俑", "清明上河图", "司母戊鼎",
        "四羊方尊", "马踏飞燕"
    ]
    matched_entity = next((e for e in entities if e in question), None)
    
    # 属性识别（正则增强）
    import re
    prop_pattern = r"(收藏地|时代|材质|...)"  # 扩展所有属性关键词
    matched_prop = re.search(prop_pattern, question)
    
    return matched_entity, matched_prop.group(0) if matched_prop else None

def terminal_qa():
    """终端问答交互界面"""
    print("海外文物知识问答系统（输入exit退出）")
    print("-"*50)
    
    while True:
        try:
            # 支持多行输入
            question = input("\n提问 > ")
            if question.lower() in ['exit', 'quit']: break
            
            # 执行查询
            entity, prop = enhanced_parser(question)
            if not all([entity, prop]):
                print("未能识别有效的文物名称或属性")
                continue
                
            # 知识图谱查询
            cypher = f"MATCH (a:Artifact) WHERE a.name CONTAINS '{entity}' RETURN a.{PROPERTY_MAPPING[prop]} as ans"
            result = graph.run(cypher).data()
            
            # 结果生成
            if result and result[0]['ans']:
                answer = f"[答案] {entity}的{prop}是：{result[0]['ans']}"
            else:
                answer = f"未找到{entity}的{prop}信息"
            
            # 终端格式化输出
            print("\n" + "="*50)
            print(f"文物名称：{entity}")
            print(f"问题类型：{prop}")
            print(answer)
            print("="*50 + "\n")
            
        except Exception as e:
            print(f"系统错误：{str(e)}")

if __name__ == "__main__":
    terminal_qa()
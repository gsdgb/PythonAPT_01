import os
import random
import torch
from torch_geometric.data import Dataset, Data
from torch_geometric.utils import barabasi_albert_graph, erdos_renyi_graph

# 配置参数（与现有模型兼容）
NUM_SAMPLES = 1000  # 总样本数
NUM_NODES = 50  # 每个图的平均节点数
NUM_EDGES = 100  # 每个图的平均边数
NUM_NODE_ATTR = 10  # 节点属性维度（与model_RGAT.py匹配）
NUM_EDGE_ATTR = 114  # 边属性维度（与darpa数据集匹配）
SAVE_DIR = "./simulated_dataset"  # 保存路径


class SimulatedAPTDataset(Dataset):
    def __init__(self, root, transform=None, pre_transform=None):
        self.root = root
        super().__init__(root, transform, pre_transform)

    @property
    def raw_dir(self):
        return os.path.join(self.root, "raw")

    @property
    def processed_dir(self):
        return os.path.join(self.root, "processed")

    @property
    def raw_file_names(self):
        return []  # 无原始文件，直接生成

    @property
    def processed_file_names(self):
        return [f"sim_graph_{i}.pt" for i in range(NUM_SAMPLES)]

    def generate_normal_graph(self):
        """生成正常图（负样本）：规则结构，属性分布集中"""
        # 随机节点数（围绕均值波动）
        num_nodes = random.randint(NUM_NODES - 10, NUM_NODES + 10)
        # 修复：barabasi_albert_graph不支持directed参数，移除该参数
        edge_index = barabasi_albert_graph(num_nodes, 5)  # 生成无向图（符合函数默认行为）

        # 节点属性：集中在0~3（正常范围）
        x = torch.randint(0, 4, (num_nodes, NUM_NODE_ATTR), dtype=torch.long)

        # 边属性：集中在0~50（正常关系类型）
        edge_attr = torch.randint(0, 50, (edge_index.shape[1], 1), dtype=torch.long)

        # 标签：0（正常）
        y = torch.tensor([0], dtype=torch.float)

        return Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y)

    def generate_abnormal_graph(self):
        """生成异常图（正样本）：包含结构异常和属性异常"""
        # 基础结构用随机图（结构异常）
        num_nodes = random.randint(NUM_NODES - 5, NUM_NODES + 15)
        # erdos_renyi_graph支持directed参数，保持不变
        edge_index = erdos_renyi_graph(num_nodes, 0.3, directed=True)

        # 节点属性：包含异常值（5~9）
        x = torch.randint(0, 4, (num_nodes, NUM_NODE_ATTR), dtype=torch.long)
        abnormal_nodes = random.sample(range(num_nodes), k=num_nodes // 5)
        x[abnormal_nodes] = torch.randint(5, 10, (len(abnormal_nodes), NUM_NODE_ATTR), dtype=torch.long)

        # 边属性：包含异常关系类型（50~113）
        edge_attr = torch.randint(0, 50, (edge_index.shape[1], 1), dtype=torch.long)
        abnormal_edges = random.sample(range(edge_index.shape[1]), k=edge_index.shape[1] // 4)
        edge_attr[abnormal_edges] = torch.randint(50, 114, (len(abnormal_edges), 1), dtype=torch.long)

        # 标签：1（异常）
        y = torch.tensor([1], dtype=torch.float)

        return Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y)

    def process(self):
        # 创建保存目录
        os.makedirs(self.processed_dir, exist_ok=True)

        # 生成样本（正负样本比例1:1）
        for i in range(NUM_SAMPLES):
            if i % 2 == 0:
                graph = self.generate_normal_graph()
            else:
                graph = self.generate_abnormal_graph()

            # 应用预处理（如果有）
            if self.pre_transform is not None:
                graph = self.pre_transform(graph)

            # 保存图数据
            torch.save(graph, os.path.join(self.processed_dir, f"sim_graph_{i}.pt"))
            if (i + 1) % 100 == 0:
                print(f"已生成 {i + 1}/{NUM_SAMPLES} 个样本")

    def len(self):
        return NUM_SAMPLES

    def get(self, idx):
        return torch.load(os.path.join(self.processed_dir, f"sim_graph_{idx}.pt"))


if __name__ == "__main__":
    # 生成数据集
    dataset = SimulatedAPTDataset(root=SAVE_DIR)
    print(f"数据集生成完成，共 {len(dataset)} 个样本")

    # 验证样本格式
    sample = dataset[0]
    print("\n样本结构验证：")
    print(f"节点特征 shape: {sample.x.shape}")
    print(f"边索引 shape: {sample.edge_index.shape}")
    print(f"边属性 shape: {sample.edge_attr.shape}")
    print(f"标签: {sample.y.item()} (0=正常, 1=异常)")

    # 统计正负样本比例
    pos_count = sum(1 for i in range(len(dataset)) if dataset[i].y.item() == 1)
    print(f"\n正样本比例: {pos_count}/{len(dataset)} ({pos_count / len(dataset):.2f})")

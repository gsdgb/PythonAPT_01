import json
import os
import random
from datetime import datetime, timedelta

# 模拟DARPA数据集的结构：包含主机、对象（文件/进程等）、事件
def generate_darpa_simulated_data(output_dir, num_objects=1000, num_events=10000):
    os.makedirs(output_dir, exist_ok=True)
    object_json_path = os.path.join(output_dir, "darpa-tc-cadets-object.json")
    event_json_path = os.path.join(output_dir, "darpa-tc-cadets-event.json")

    # 主机UUID（对应代码中的host_uuid）
    host_uuids = ["A3702F4C-5A0C-11E9-B8B9-D4AE52C1DBD3",
                  "3A541941-5B04-11E9-B2DB-D4AE52C1DBD3",
                  "CB02303B-654E-11E9-A80C-6C2B597E484C"]
    host_id_map = {uuid: i for i, uuid in enumerate(host_uuids)}

    # 节点类型（对应node_type_list）
    node_types = ['FILE_OBJECT_DIR', 'FILE_OBJECT_FILE', 'FILE_OBJECT_UNIX_SOCKET',
                  'IPC_OBJECT_PIPE_UNNAMED', 'IPC_OBJECT_SOCKET_PAIR',
                  'com.bbn.tc.schema.avro.cdm20.NetFlowObject', 'PRINCIPAL_LOCAL',
                  'SRCSINK_IPC', 'SUBJECT_PROCESS']

    # 事件类型（对应event_type_list）
    event_types = ["EVENT_ACCEPT", "EVENT_OPEN", "EVENT_READ", "EVENT_WRITE",
                   "EVENT_EXECUTE", "EVENT_CONNECT", "EVENT_SENDTO", "EVENT_RECVFROM"]

    # 生成对象数据（供create_object_database.py解析）
    objects = []
    for i in range(num_objects):
        host_uuid = random.choice(host_uuids)
        obj_type = random.choice(node_types)
        obj = {
            "hostId": host_uuid,
            "datum": {
                obj_type: {  # 随机一种对象类型
                    "uuid": f"obj_{i}_{host_id_map[host_uuid]}",
                    "type": obj_type
                }
            }
        }
        objects.append(obj)

    with open(object_json_path, "w", encoding="utf-8") as f:
        for obj in objects:
            f.write(json.dumps(obj) + "\n")

    # 生成事件数据（用于构建溯源图）
    events = []
    start_time = datetime(2019, 5, 17)
    for i in range(num_events):
        host_uuid = random.choice(host_uuids)
        event_type = random.choice(event_types)
        # 随机时间（模拟分钟级时间戳）
        timestamp = (start_time + timedelta(minutes=random.randint(0, 100))).timestamp() * 1e9  # 纳秒
        # 随机主体和对象UUID
        subject_uuid = f"subj_{random.randint(0, num_objects//2)}_{host_id_map[host_uuid]}"
        obj1_uuid = f"obj_{random.randint(0, num_objects-1)}_{host_id_map[host_uuid]}"
        obj2_uuid = f"obj_{random.randint(0, num_objects-1)}_{host_id_map[host_uuid]}" if random.random() > 0.5 else None

        event = {
            "hostId": host_uuid,
            "datum": {
                "com.bbn.tc.schema.avro.cdm20.Event": {
                    "type": event_type,
                    "subject": {"com.bbn.tc.schema.avro.cdm20.UUID": subject_uuid},
                    "predicateObject": {"com.bbn.tc.schema.avro.cdm20.UUID": obj1_uuid},
                    "predicateObject2": {"com.bbn.tc.schema.avro.cdm20.UUID": obj2_uuid} if obj2_uuid else None,
                    "timestampNanos": int(timestamp)
                }
            }
        }
        events.append(event)

    with open(event_json_path, "w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")

    print(f"模拟DARPA数据集已生成至 {output_dir}")


#### 2. 模拟 StreamSpot 数据集生成脚本
def generate_streamspot_simulated_data(output_dir, num_graphs=500):
    os.makedirs(output_dir, exist_ok=True)
    tsv_path = os.path.join(output_dir, "all.tsv")

    # 节点属性（a-e对应5种节点类型）
    node_chars = [chr(ord('a') + i) for i in range(5)]
    # 边属性（f-z、A-H对应29种边类型）
    edge_chars = [chr(ord('f') + i) for i in range(21)] + [chr(ord('A') + i) for i in range(8)]

    with open(tsv_path, "w", encoding="utf-8") as f:
        for graph_num in range(num_graphs):
            # 每个图生成100-500条边
            num_edges = random.randint(100, 500)
            for _ in range(num_edges):
                src_node = random.randint(0, 100)
                src_attr = random.choice(node_chars)
                dst_node = random.randint(0, 100)
                dst_attr = random.choice(node_chars)
                edge_attr = random.choice(edge_chars)
                # TSV格式：src_node  src_attr  dst_node  dst_attr  edge_attr  graph_num
                f.write(f"{src_node}\t{src_attr}\t{dst_node}\t{dst_attr}\t{edge_attr}\t{graph_num}\n")

    print(f"模拟StreamSpot数据集已生成至 {output_dir}")


if __name__ == "__main__":
    # 生成模拟DARPA数据集（用于darpa-tc-cadets目录）
    generate_darpa_simulated_data(output_dir="darpa-tc-cadets/simulated_darpa")
    # 生成模拟StreamSpot数据集
    # generate_streamspot_simulated_data(output_dir="streamspot")
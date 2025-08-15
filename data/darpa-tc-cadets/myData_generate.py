import json
import uuid
import random


# 生成示例数据集，每行一个独立的JSON对象
def generate_sample_dataset(filename="darpa-tc-cadets-object.json", num_records=1000):
    host_ids = ["A3702F4C-5A0C-11E9-B8B9-D4AE52C1DBD3",
                "3A541941-5B04-11E9-B2DB-D4AE52C1DBD3",
                "CB02303B-654E-11E9-A80C-6C2B597E484C"]

    object_types = [
        "com.bbn.tc.schema.avro.cdm20.FileObject",
        "com.bbn.tc.schema.avro.cdm20.Subject",
        "com.bbn.tc.schema.avro.cdm20.NetFlowObject",
        "com.bbn.tc.schema.avro.cdm20.Principal",
        "com.bbn.tc.schema.avro.cdm20.Host"
    ]

    file_object_types = ['FILE_OBJECT_DIR', 'FILE_OBJECT_FILE', 'FILE_OBJECT_UNIX_SOCKET',
                         'IPC_OBJECT_PIPE_UNNAMED', 'IPC_OBJECT_SOCKET_PAIR',
                         'com.bbn.tc.schema.avro.cdm20.NetFlowObject', 'PRINCIPAL_LOCAL',
                         'SRCSINK_IPC', 'SUBJECT_PROCESS']

    with open(filename, "w", encoding="utf-8") as f:
        for i in range(num_records):
            host_id = random.choice(host_ids)

            # 随机选择对象类型
            obj_type = random.choice(object_types)

            # 生成UUID
            obj_uuid = str(uuid.uuid4())

            if obj_type == "com.bbn.tc.schema.avro.cdm20.Subject":
                # Subject类型对象
                parent_subject = str(uuid.uuid4()) if random.random() > 0.3 else None
                local_principal = str(uuid.uuid4()) if random.random() > 0.2 else None

                record = {
                    "hostId": host_id,
                    "datum": {
                        obj_type: {
                            "uuid": obj_uuid,
                            "type": random.choice(file_object_types),
                            "parentSubject": {
                                "com.bbn.tc.schema.avro.cdm20.UUID": parent_subject} if parent_subject else None,
                            "localPrincipal": {
                                "com.bbn.tc.schema.avro.cdm20.UUID": local_principal} if local_principal else None
                        }
                    }
                }
            elif obj_type == "com.bbn.tc.schema.avro.cdm20.Host":
                # Host类型对象
                record = {
                    "hostId": host_id,
                    "datum": {
                        obj_type: {
                            "uuid": obj_uuid
                        }
                    }
                }
            else:
                # 其他类型对象
                record = {
                    "hostId": host_id,
                    "datum": {
                        obj_type: {
                            "uuid": obj_uuid,
                            "type": random.choice(file_object_types)
                        }
                    }
                }

            # 每个JSON对象占一行
            f.write(json.dumps(record, separators=(',', ':')) + "\n")

    print(f"生成了 {num_records} 条记录到 {filename}")


# 生成示例数据集
generate_sample_dataset("darpa-tc-cadets-object.json", 100)

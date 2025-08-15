import sqlite3


def verify_database():
    print("=== 数据库验证 ===")
    conn = sqlite3.connect("cadets-database.db")
    cur = conn.cursor()

    try:
        # 检查objects表数据量
        cur.execute("SELECT COUNT(*) FROM objects")
        objects_count = cur.fetchone()[0]
        print(f"Objects表记录数: {objects_count}")

        # 检查subjects表数据量
        cur.execute("SELECT COUNT(*) FROM subjects")
        subjects_count = cur.fetchone()[0]
        print(f"Subjects表记录数: {subjects_count}")

        # 显示一些示例数据
        if objects_count > 0:
            print("\nObjects表示例数据:")
            cur.execute("SELECT * FROM objects LIMIT 5")
            for row in cur.fetchall():
                print(f"  UUID: {row[0]}, Host: {row[1]}, Type: {row[2]}")

        if subjects_count > 0:
            print("\nSubjects表示例数据:")
            cur.execute("SELECT * FROM subjects LIMIT 5")
            for row in cur.fetchall():
                print(f"  UUID: {row[0]}, Host: {row[1]}, Parent: {row[2]}, Principal: {row[3]}")

    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
    finally:
        cur.close()
        conn.close()
        print("=== 验证完成 ===")


if __name__ == "__main__":
    verify_database()

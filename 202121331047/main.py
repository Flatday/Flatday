from collections import Counter
import jieba
import sys


def getSimilarity(setX: Counter, setY: Counter):
    intersection = (setX & setY).values()  # 求交集
    union = (setX | setY).values()  # 求并集
    similarity = 100*sum(intersection)/sum(union)  # 计算相似度
    return similarity


try:
    oriPath, copyPath, resultPath = sys.argv[1:4]  # 命令行参数

    with open(oriPath, "r", encoding="utf-8") as f:  # 读取原始文件
        ori = f.read()

    with open(copyPath, "r", encoding="utf-8") as f:  # 读取抄袭文件
        copy = f.read()

    oriWord, copyWord = map(Counter, [ori, copy])  # 统计字频
    oriCut, copyCut = map(Counter, map(jieba.cut, [ori, copy]))  # 统计词频

    with open(resultPath, "w+", encoding="utf-8") as f:
        f.write(f"基于字频相似度: {getSimilarity(oriWord,copyWord):.2f}%\n")  # 保存结果
        f.write(f"基于词频相似度: {getSimilarity(oriCut,copyCut):.2f}%")  # 保存结果

except ValueError as e:  # 命令行参数异常
    print(e.with_traceback())
    print(f"Usage: python {sys.argv[0]} 原文文件路径 抄袭文件路径 结果输出路径")
except FileNotFoundError as e:  # 文件不存在异常
    print(f"路径 {e.filename} 不存在")
except ZeroDivisionError as e:  # 文件内容都为空
    with open(resultPath, "w+", encoding="utf-8") as f:
        f.write(f"均为空白文件")  # 保存结果
except Exception as e:
    print(e)

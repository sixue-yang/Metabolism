# _author_ = 'sixueyang'
# _date_ = 2023/10/19 16:11
import argparse
import os
import pandas as pd
from itertools import combinations
import subprocess as sp


# 设置传参
def get_args():
    parser = argparse.ArgumentParser(description="代谢组分析 - 数据预处理")
    parser.add_argument("-c", "--compare", help="组间比较列表", default=None)
    parser.add_argument("-o", "--output", help="两两组合比较列表", required=True)
    parser.add_argument("-g", "--group", help="分组文件", required=True)
    return parser.parse_args()


if __name__ == '__main__':
    argv = get_args()
    compare_path = argv.compare
    output = argv.output
    group_list = argv.group

    if not compare_path or not os.path.exists(compare_path):
        group_df = pd.read_csv(group_list,sep='\t',header=None)
        groups = sorted(list(set(group_df[1].tolist())))
        try:
            groups.remove('QC')
        except:
            pass
        # print(groups)
        with open(output,'w') as out_obj:
            for one,two in combinations(groups,2):
                print('\t'.join(map(str,[one,two])),file=out_obj)
    else:
        cmd = f'ln -f {compare_path} {output}'
        sp.call(cmd,shell=True)

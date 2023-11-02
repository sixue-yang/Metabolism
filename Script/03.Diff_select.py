# _author_ = 'sixueyang'
# _date_ = 2023/10/8 14:38
import pandas as pd
import argparse
import numpy as np
from collections import Counter

# TODO:筛选差异代谢物，输出用于绘制表达聚类热图及火山图的数据


def get_argv():
    parser = argparse.ArgumentParser(description="代谢组分析 - 差异分析代谢物筛选")
    parser.add_argument("-i", "--input", help="分组提取后数据", required=True)
    parser.add_argument("-d", "--diff", help="各种检验计算后的值", required=True)
    parser.add_argument("-pc", "--pvalue_cutoff", help="P-value 阈值",type=float, default=0.05)
    parser.add_argument("-fc", "--fold_change_cutoff", help="fold-change 阈值",type=float, default=1.0)
    parser.add_argument("-vip", "--vip_cutoff", help="pls-da分析结果 vip阈值", type=float,default=1)
    parser.add_argument("-o1", "--output_cor", help="输出用于差异热图绘制文件", required=True)
    parser.add_argument("-o2", "--output_vol", help="输出用于火山图绘制文件", required=True)
    return parser.parse_args()

# 计算-log10
def count_log(value):
    return -np.log10(value)

# 修改值
def change_dic(dic:dict):
    for key in dic:
        dic[key] = f'{key} {dic[key]}'
    return dic


if __name__ == '__main__':
    # 设置参数
    argv = get_argv()
    input_file = argv.input
    diff_count_file = argv.diff
    pvalue_cutoff = argv.pvalue_cutoff
    fold_change_cutoff = argv.fold_change_cutoff

    vip_cutoff = argv.vip_cutoff
    output_cor = argv.output_cor
    output_vol = argv.output_vol


    A_df = pd.read_csv(input_file,sep='\t',index_col=0)
    diff_count_df = pd.read_csv(diff_count_file,sep='\t')

    # 根据阈值筛选代谢物
    DEM_df = diff_count_df[(diff_count_df['pvalue']<=pvalue_cutoff)&(diff_count_df['vipVn'] >= vip_cutoff)&((diff_count_df['log2fc']<=-fold_change_cutoff)|(diff_count_df['log2fc']>=fold_change_cutoff))]

    out_cols = ['Group']
    out_cols.extend(DEM_df['metabolin'].tolist())
    out_df = A_df.loc[:,out_cols]
    out_df.to_csv(output_cor,sep='\t')

    # 处理火山图绘制数据
    diff_count_df['flog10_pvalue'] = diff_count_df['pvalue'].map(count_log)
    # 鉴定上下调代谢物及非显著代谢物
    types = []
    for row in diff_count_df.index:
        pvalue = diff_count_df.loc[row,'pvalue']
        log2fc = diff_count_df.loc[row,'log2fc']
        vips = diff_count_df.loc[row,'vipVn']
        if pvalue >= pvalue_cutoff or vips < vip_cutoff:
            types.append('NoSig')
        else:
            if log2fc >= fold_change_cutoff:
                types.append('Up')
            elif log2fc <= -fold_change_cutoff:
                types.append('Down')
            else:
                types.append('NoSig')
    diff_count_df['types'] = types
    type_count = Counter(types)
    type_count_dic = change_dic(type_count)
    diff_count_df['type2'] = diff_count_df['types'].map(type_count_dic)
    diff_count_df.to_csv(output_vol,sep='\t',index=False,header=True)

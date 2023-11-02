# _author_ = 'sixueyang'
# _date_ = 2023/10/16 16:40
import pandas as pd
import argparse
from collections import defaultdict


# TODO:提取差异代谢物列表数据，准备绘制分面小提琴图


# 设置参数
def get_argv():
    parser = argparse.ArgumentParser(description="代谢组分析 - 差异分析代谢物小提琴图数据整理")
    parser.add_argument("-i", "--diffexp", help="提取的两组差异代谢物", required=True)
    parser.add_argument("-o", "--output_vio", help="输出用于小提琴图绘制文件", required=True)
    return parser.parse_args()


if __name__ == '__main__':
    argv = get_argv()
    diff_file = argv.diffexp
    out_data = argv.output_vio
    exp_df = pd.read_csv(diff_file,sep='\t',index_col=0)

    sort_dic = defaultdict(list)
    for col in exp_df.columns[1:]:
        for row in exp_df.index:
            sort_dic['Group'].append(exp_df.loc[row,'Group'])
            sort_dic['metabolite'].append(col)
            sort_dic['value'].append(exp_df.loc[row,col])
    sort_df = pd.DataFrame(sort_dic)
    sort_df.to_csv(out_data,sep='\t',index=False)







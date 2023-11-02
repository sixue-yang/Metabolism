# _author_ = 'sixueyang'
# _date_ = 2023/9/27 16:02
import pandas as pd
import argparse


# TODO:拆分各组数据,用于后续差异分析


def get_argv():
    parser = argparse.ArgumentParser(description="代谢组分析 - 差异分析数据拆分")
    parser.add_argument("-i", "--input", help="数据预处理后矩阵", required=True)
    parser.add_argument("-t", "--treat", help="实验组", required=True)
    parser.add_argument("-c", "--control", help="对照组", required=True)
    parser.add_argument("-o", "--output", help="提取数据", required=True)
    return parser.parse_args()


# 获取各组代谢物存在完全一致的值
def get_drop_mata(data:pd.DataFrame):
    unique_counts = data.nunique()
    # 选择要删除的列
    return list(unique_counts[unique_counts == 1].index)


if __name__ == '__main__':

    # 参数设置
    argv = get_argv()
    file = argv.input
    treat = argv.treat
    control = argv.control
    out_file = argv.output
    data_df = pd.read_csv(file,sep='\t',index_col=0)
    out_df = data_df[(data_df['Group'] == treat)|(data_df['Group'] == control)]
    # 删除数据框中值完全一致的列
    drop_list = get_drop_mata(out_df[out_df['Group'] == treat])

    drop_list.extend(get_drop_mata(out_df[out_df['Group'] == control]))

    # 选择要删除的列    
    columns_to_drop = list(set(drop_list))
    columns_to_drop.remove('Group')
    # 删除选定的列
    out_df.drop(columns_to_drop, axis=1, inplace=True)
    out_df.to_csv(out_file,sep='\t')








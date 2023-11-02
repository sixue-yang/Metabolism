# _author_ = 'sixueyang'
# _date_ = 2023/10/17 11:04
import pandas as pd
import argparse
from sklearn.preprocessing import StandardScaler

# TODO:对差异代谢物进行标准化，生成Z-score散点图对应的数据

# 设置参数
def get_argv():
    parser = argparse.ArgumentParser(description="代谢组分析 - 差异分析代谢物Z-score散点图数据整理")
    parser.add_argument("-i", "--sortdata", help="小提琴图绘制文件", required=True)
    parser.add_argument("-o", "--output_z", help="输出用于Z-score图绘制文件", required=True)
    return parser.parse_args()



if __name__ == '__main__':

    argv = get_argv()
    file = argv.sortdata
    out_data = argv.output_z

    data = pd.read_csv(file,sep='\t')
    group = data.groupby('metabolite')

    scaler_list = []
    flag = 1
    for meta,meta_else in group:
        if flag >= 51:
            break
        scaler = StandardScaler()
        meta_else['value'] = scaler.fit_transform(meta_else['value'].to_numpy().reshape(-1, 1)).ravel().tolist()
        scaler_list.append(meta_else)
        flag += 1
    scaler_df = pd.concat(scaler_list,axis=0)
    scaler_df.to_csv(out_data,sep='\t',index=False)



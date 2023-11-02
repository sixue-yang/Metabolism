# _author_ = 'sixueyang'
# _date_ = 2023/10/30 11:57
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from collections import Counter,defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import argparse


# 构建对应类别字典
def mk_cluster_dic(cluster_label,rawmeta):
    cluster_dic = defaultdict(list)
    for key,value in zip(cluster_label,rawmeta):
        cluster_dic[key].append(value)
    return cluster_dic


# 对各组各个代谢物求和处理
def group_sum(data:pd.DataFrame):
    # groups = []
    sum_datas = []
    group_g = data.groupby('Group')
    for g_name,g_else in group_g:
        sum_df = pd.DataFrame(g_else.loc[:,g_else.columns[:-1]].sum(axis=0),columns=[g_name])
        sum_datas.append(sum_df)
    sum_dfs = pd.concat(sum_datas,axis=1)
    return sum_dfs


# 绘图
def line_plot(data:pd.DataFrame,clu_dic,count_dic,n_clusters:int,colors:list,outplot):
    lens = int(np.sqrt(n_clusters))
    fig, axes = plt.subplots(lens, lens, figsize=(10, 8))
    x = 0
    y = 0
    for i in range(n_clusters):
        if i >= lens:
            x = 0
            y += 1
            lens += lens
        ax = axes[x,y]
        for col in clu_dic[i]:
            ax.plot(data.index, data[col], color=colors[i], alpha=0.5, linewidth=3)
        ax.plot(data.index, centroids[i], color='black', linewidth=4)
        ax.set_xticklabels(data.index, rotation=90)
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')
        title = f'Cluster{i+1},{count_dic[i]} metabolites'
        ax.set_title(title)
        ax.set_ylabel('Standerised Intensity')
        #Standerised Intensity
        x += 1
    # plt.ylabel()
    plt.tight_layout()
    plt.savefig(outplot)


# 设置参数
def get_argv():
    parser = argparse.ArgumentParser(description="代谢组分析 - Kmeans 聚类分析")
    parser.add_argument("-i", "--normalization", help="归一化后的数据", required=True)
    parser.add_argument("-n", "--n_clusters", help="聚类的数量", type=int,default=9)
    parser.add_argument("-op", "--out_plot", help="聚类绘图文件", required=True)
    parser.add_argument("-od", "--out_data", help="聚类结果文件", required=True)
    return parser.parse_args()


if __name__ == '__main__':
    argv = get_argv()

    file = argv.normalization
    n_clusters = argv.n_clusters
    out_plot = argv.out_plot
    out_data = argv.out_data
    # 从 Seaborn 调色板中提取指定数量的颜色
    colors = sns.color_palette('bright', n_colors=n_clusters)
    data = pd.read_csv(file,sep='\t',index_col=0)
    clean_data = data[data['Group'] != 'QC']
    sum_dfs = group_sum(clean_data)
    # analysis_df = clean_data.loc[:,clean_data.columns[:-1]]

    # 数据标准化
    scaler = StandardScaler()
    scaler_df = pd.DataFrame(scaler.fit_transform(sum_dfs),index=sum_dfs.index,columns=sum_dfs.columns)


    # 创建K-Means模型并指定簇的数量（K值）
    kmeans = KMeans(n_clusters=n_clusters)
    # 拟合模型并进行聚类
    kmeans.fit(scaler_df)
    # 获取簇中心的坐标
    centroids = kmeans.cluster_centers_

    # 预测每个数据点所属的簇
    labels = kmeans.labels_
    # print(len(labels))
    clu_dic = mk_cluster_dic(labels,scaler_df.index)
    cout_dic = Counter(labels)
    # 绘图
    line_plot(scaler_df.T,clu_dic,cout_dic,n_clusters,colors,out_plot)
    # 出表
    meta_map = dict(zip(scaler_df.index,list(map(lambda x:x+1,labels))))
    scaler_df['cluster'] = scaler_df.index.map(meta_map)
    scaler_df = scaler_df.reset_index()
    header = list(scaler_df.columns)
    header[0] = 'Metabolites'
    scaler_df.columns = header
    scaler_df.to_csv(out_data,sep='\t',index=False)
    # print(scaler_df)













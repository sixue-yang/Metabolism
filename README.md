# Metabolism
Metabolome analysis process based on snakemake.

本流程由代谢物定量表开始，执行代谢组高级分析。适用于Linux系统，SGE等集群。



## 快速使用

### 投递命令

```sh
python /work1/Users/yangsixue/pipline/metabolism/Script/Metabolism_main_v1.py -i [代谢物定量表] -m [缺失值填充方式] -g [样本分群文件] -a [pvalue 矫正方法] -S [kegg分析 模式物种缩写] -n [kmeans聚类簇数量]
```

### 主脚本参数说明

```sh
usage: Metabolism_main_v1.py [-h] -i INPUT [-m {KNN,min,median,mean}] [-c COMPARE_LIST] [-db DBPATH] -g GROUP [-a ADJUST_MODEL] [-n N_CLUSTER] [-S SPE] [-job MAX_JOBS] [-wt WAIT_TIME]
                             [-sn SNAKEMAKE]

代谢组 - 高级分析

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        下机比对数据
  -m {KNN,min,median,mean}, --miss_model {KNN,min,median,mean}
                        缺失值填充方法
  -c COMPARE_LIST, --compare_list COMPARE_LIST
                        比较组合列表
  -db DBPATH, --dbpath DBPATH
                        数据库所在路径 若数据库文件不存在会自动填充
  -g GROUP, --group GROUP
                        样本分群文件
  -a ADJUST_MODEL, --adjust_model ADJUST_MODEL
                        p-value 矫正方法
  -n N_CLUSTER, --n_cluster N_CLUSTER
                        kmeans 聚类簇数量
  -S SPE, --spe SPE     KEGG 建库使用的物种缩写
  -job MAX_JOBS, --max_jobs MAX_JOBS
                        最大并行任务数，默认100
  -wt WAIT_TIME, --wait_time WAIT_TIME
                        任务执行后等待结果的时间，默认300秒
  -sn SNAKEMAKE, --snakemake SNAKEMAKE
                        snakemake软件路径
```

### 输入数据格式

* 代谢物定量表 -- xlsx文件格式

| id                                   | NAME_EN           | NAME_CH    | CAS        | KEGG_ID | FORMULA   | EXACT_MASS | CLASS_EN             | CLASS_CH      | q1    | q3    | ionmode | rt   | 1-QC-01(样本列往后顺延) |
| ------------------------------------ | ----------------- | ---------- | ---------- | ------- | --------- | ---------- | -------------------- | ------------- | ----- | ----- | ------- | ---- | ----------------------- |
| STD_21293-29-8@-@RANK1               | (+)-Abscisic acid | 脱落酸     | 21293-29-8 | C06082  | C15H20O4  | 264.1362   | phytohormone         | 植物激素      | 263   | 153   | -       | 7.86 | 1491842.063             |
| STD_468-44-0@-@RANK1                 | Gibberellin A4    | 赤霉素A4   | 468-44-0   | C11864  | C19H24O5  | 332.1624   | phytohormone         | 植物激素      | 331   | 243   | -       | 9.98 | 916.426                 |
| STD_29838-67-3@-@RANK1               | Astilbin          | 落新妇苷   | 29838-67-3 | C17449  | C21H22O11 | 450.1162   | flavonoids           | 类黄酮        | 448.9 | 302.8 | -       | 6.23 | 9283.725                |
| STD_572-30-5@-@RANK1                 | Avicularin        | 扁蓄苷     | 572-30-5   |         | C20H18O11 | 434.084911 | flavonoids           | 类黄酮        | 432.9 | 300.4 | -       | 6.47 | 1204419.81              |
| STD_520-26-3@-@RANK1                 | Hesperidin        | 橙皮苷     | 520-26-3   | C09755  | C28H34O15 | 610.1898   | flavonoids           | 类黄酮        | 609   | 300.8 | -       | 6.65 | 4258.1705               |
| STD_482-38-2@-@RANK1                 | Kaempferitrin     | 山奈苷     | 482-38-2   | C16981  | C27H30O14 | 578.1636   | flavonoids           | 类黄酮        | 577.5 | 431.7 | -       | 6.09 | 9742.047999             |
| STD_604-80-8@-@RANK1                 | Narcissoside      | 水仙苷     | 604-80-8   |         | C28H32O16 | 624.169035 | flavonoids           | 类黄酮        | 622.9 | 314.9 | -       | 6.38 | 31673.249               |
| STD_522-12-3@-@RANK1                 | Quercitrin        | 槲皮苷     | 522-12-3   | C01750  | C21H20O11 | 448.1006   | flavonoids           | 类黄酮        | 446.9 | 300.8 | -       | 6.59 | 218223.0145             |
| STD_72063-39-9@-@RANK1               | Spinosin          | 斯皮诺素   | 72063-39-9 | C17834  | C28H32O15 | 608.1741   | flavonoids           | 类黄酮        | 607.5 | 606.8 | -       | 5.79 | 4811.1                  |
| STD_77026-92-7@-@RANK1               | (±)-Jasmonic acid | (±)-茉莉酸 | 77026-92-7 | C08491  | C12H18O3  | 210.1256   | phytohormone         | 植物激素      | 209   | 59    | -       | 8.94 | 33149.6145              |
| 616@[M-H]-@RANK1;STD_69-72-7@-@RANK1 | Salicylic acid    | 水杨酸     | 69-72-7    | C00805  | C7H6O3    | 138.031695 | Phenols;phytohormone | 酚类;植物激素 | 137   | 93    | -       | 7.06 | 44330.2575              |

* 样本分群文件 -- txt格式 第一列为样本信息，第二列为所属群，列与列间使用tab键分隔，无表头

| 1-QC-01     | QC   |
| ----------- | ---- |
| 2-QC-02     | QC   |
| 3-QC-03     | QC   |
| 4-QC-04     | QC   |
| H5_HS_2_E_1 | D    |
| H5_HS_2_E_2 | D    |

* 比较组合列表 -- txt格式 第一列为对照组，第二列为处理组 列与列间使用tab键分隔，无表头

| A    | B    |
| ---- | ---- |
| A    | C    |
| A    | D    |
| A    | E    |
| A    | F    |



### 结果目录结构说明

```sh
├── 00.Bin                                        # 存放执行过程中 每一步命令
├── 01.Data_prepare                               # 数据预处理 整体PCA、PLS-DA、K-mean分析结果
│   ├── All.normalization.xls                     # 数据预处理结果
│   ├── All.pca2d.pdf                             # 整体数据二维PCA结果
│   ├── All.pca3d.pdf                             # 整体数据三维PCA结果
│   ├── All.plsda.pdf                             # 整体数据plsda分析结果
│   ├── change_id.log                             # 代谢物名称、转化后ID、kegg ID对应表
│   ├── compare.list                              # 比较组合列表
│   ├── KMeans_Analysis_data_matrix.xls           # KMeans聚类 分析结果对应表
│   └── KMeans_Plot.pdf                           # KMean聚类分析结果
├── 02.Diff_analysis                              # 比较差异分析目录
│   ├── *                                         # 每一种比较组合分析目录
│   │   ├── *_cor_heatmap.pdf                     # 代谢物相关性分析热图
│   │   ├── *_DEP_exp.xls                         # 差异代谢物表达矩阵
│   │   ├── *_Diff_count.xls                      # 差异分析计算结果 -- 每一种代谢物对一个的组间p-value、q-value、VIP、fold-change等
│   │   ├── *_diff_value.xls                      # 差异分析计算结果显著性，上调、下调注释
│   │   ├── *_heatmap.pdf                         # 代谢物表达量热图
│   │   ├── *_log2fc_hbar.pdf                     # 差异代谢物 log2FC 水平柱状图 -- 上调和下调分别选取top 10绘制
│   │   ├── *.normalization.xls                   # 两组代谢物预处理结果
│   │   ├── *_oplsda.pdf                          # PLS-DA 分析结果
│   │   ├── *.pca2d.pdf                           # 组间 二维PCA散点图
│   │   ├── *.pca3d.pdf                           # 组间 三维PCA散点图
│   │   ├── *.plsda.pdf                           # 组间 PLS-DA散点图
│   │   ├── *_violin.pdf                          # 组间差异代谢物小提琴图
│   │   ├── *_violin_plot.xls                     # 组间小提琴图绘制文件
│   │   ├── *_vip_point.pdf                       # VIP 散点图
│   │   ├── *_volcano.pdf                         # 组间 火山图
│   │   ├── *_zscore.pdf                          # 组间差异代谢物 Z-score分布图
│   │   └── *_zscore.xls                          # 组间 Z-score分布图绘制文件
├── 03.KEGG_Enrichment                            # KEGG富集分析
│   ├── *                                         # 每一种组合 KEGG富集分析目录
│   │   ├── *_barplot.pdf                         # KEGG富集分析 柱状图
│   │   ├── *_cnetplot.pdf                        # 代谢物与通路关系图
│   │   ├── *_diff.id                             # 差异代谢物ID
│   │   ├── *_dotplot.pdf                         # KEGG分析 气泡图
│   │   └── *_KEGG_enrichment_result.xls          # KEGG富集结果
├── 04.KEGG_Pathway                               # KEGG通路分析
│   ├── *                                         # 每一种组合 富集结果对应的通路图
├── 05.Venn                                       # 韦恩图
│   ├── diff_meta_plot.xls                        # upset 韦恩图绘制数据
│   ├── diff_meta_result.xls                      # 各组差异分析差异代谢物汇总结果
│   └── upset.pdf                                 # upset 韦恩图
├── 06.Result                                     # 分析结果整理
│   ├── 01.Statistical_Analysis                   # 统计分析结果
│   │   ├── *                                     # 存放各组统计分析结果
│   │   │   ├── *_diff_value.xls                  # 差异分析计算结果显著性，上调、下调注释
│   │   │   ├── *.pca2d.pdf                       # 各层级 二维PCA散点图
│   │   │   ├── *.pca3d.pdf                       # 各层级 三维PCA散点图
│   │   │   └── *.plsda.pdf                       # 各层级 PLS-DA散点图
│   ├── 02.Hierarchical_Clustering_Analysis       # 聚类分析结果
│   │   ├── *                                     # 存放各组聚类分析结果
│   │   │   ├── *_cor_heatmap.pdf                 # 各组代谢物相关性分析热图
│   │   │   └── *_heatmap.pdf                     # 代谢物表达量热图
│   ├── 03.Volcano                                # 火山图结果
│   │   ├── *                                     # 存放各组火山图结果
│   │   │   └── *_volcano.pdf                     # 各组火山图
│   ├── 04.VIP_point                              # VIP点图
│   │   ├── *                                     # 存放各组VIP点图
│   │   │   └── *_vip_point.pdf                   # VIP点图
│   ├── 05.Bar                                    # log2FC 水平柱状图结果
│   │   ├── *                                     # 存放各组 log2FC 水平柱状图
│   │   │   └── *_log2fc_hbar.pdf                 # log2FC 水平柱状图
│   ├── 06.Violin                                 # 小提琴图结果
│   │   ├── *                                     # 存放各组差异代谢物小提琴图
│   │   │   └── *_violin.pdf                      # 小提琴图
│   ├── 07.Z-score                                # Z-score 分布图
│   │   ├── *                                     # 存放各组差异代谢物 Z-score分布图
│   │   │   └── *_zscore.pdf                      # Z-score 分布图
│   ├── 08.KEGG_Enrichment                        # KEGG富集分析结果
│   │   ├── *                                     # 存放各组KEGG富集分析结果，若目录为空，则表示差异代谢物未得到富集
│   │   │   ├── *_barplot.pdf                     # KEGG富集分析 柱状图
│   │   │   ├── *_cnetplot.pdf                    # 代谢物与通路关系图
│   │   │   ├── *_diff.id                         # 差异代谢物ID列表(转化后)
│   │   │   ├── *_dotplot.pdf                     # KEGG分析 气泡图
│   │   │   └── *_KEGG_enrichment_result.xls      # KEGG富集分析结果
│   ├── 09.KEGG_Pathway                           # 存放各组KEGG通路图
│   ├── 10.Venn                                   # 存放韦恩图结果
│   │   ├── diff_meta_result.xls                  # 各组差异代谢物汇总(稀疏矩阵格式)
│   │   └── upset.pdf                             # 韦恩图
│   ├── 11.KMeans                                 # KMeans 分析结果
│   │   ├── KMeans_Analysis_data_matrix.xls       # KMeans 聚类分析结果
│   │   └── KMeans_Plot.pdf                       # Kmeans 聚类图
│   └── Map.xls                                   # 代谢物名称、转化后ID、kegg ID对应表
├── cluster_logs                                  # 报错日志
```


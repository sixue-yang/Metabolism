library(argparser, quietly=TRUE)
library(pheatmap)
library(ggplot2)

p <- arg_parser("run heatmap of metabolin")

# Add command line arguments

p <- add_argument(p, "--metabolintbale", help="metabolin_result.csv",type="character")
p <- add_argument(p,"--cellsize",help = "cell size (width, height)",type="character")
p <- add_argument(p,"--output_h",help = "heatmap output file name",type = "character")
p <- add_argument(p,"--output_c",help = "cor heatmap output file name",type = "character")

# Parse the command line arguments
argv <- parse_args(p)

metatable <- argv$metabolintbale
cellsize <-  as.numeric(argv$cellsize)
output_h <- argv$output_h
output_c <- argv$output_c


meta_all <- read.table(metatable,header = TRUE,row.names = 1)
group_list = meta_all$Group
meta <- meta_all[, !(names(meta_all) %in% c("Group"))]


### 绘制差异表达矩阵 ###
n<-t(scale(as.matrix(meta)))
## 调整极端值
n[n>4]=4
n[n< -4]= -4

width=ncol(n)
height=nrow(n)
# print(width)
# print(height)
#分组
ac=data.frame(groupList=group_list)
rownames(ac)=colnames(n) 

p1<-pheatmap(n,show_colnames =T,show_rownames = T,annotation = ac,border_color = F,cellheight = cellsize,fontsize = cellsize,cellwidth = cellsize,treeheight_row = 2*cellsize,treeheight_col = 2*cellsize,silent = T)

ggsave(p1,filename = output_h,width=((width+8)/cellsize)*0.7,height=(height/cellsize)*0.6,limitsize = FALSE)


### 绘制差异代谢物相关性热图  皮尔逊 ###
correlation_matrix <- cor(t(n), method = "pearson")
#print(correlation_matrix)
p2<-pheatmap(correlation_matrix,show_colnames =T,show_rownames = T,border_color = F,cellheight = cellsize,fontsize = cellsize,cellwidth = cellsize,treeheight_row = 2*cellsize,treeheight_col = 2*cellsize,silent = T)
ggsave(p2,filename = output_c,width=(height/cellsize)*0.7,height=(height/cellsize)*0.7,limitsize = FALSE)

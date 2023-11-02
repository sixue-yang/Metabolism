library(argparser, quietly=TRUE)
library(ggplot2)


p <- arg_parser("run VIP Point Plot")

# Add command line arguments


p <- add_argument(p, "--allmetabolintbale", help="all_meta_result.csv",type="character")
p <- add_argument(p,"--output",help = "output file name",type = "character")
p <- add_argument(p,"--titlename",help = "title name",type = "character")

argv <- parse_args(p)

metatable <- argv$allmetabolintbale
output <- argv$output
titlename <- argv$titlename
meta_all <- read.table(metatable,header = TRUE,sep='\t')
meta_all <- meta_all[meta_all$types != "NoSig", ]
sorted_data <- meta_all[order(meta_all$vipVn, decreasing = TRUE), ]


top_20_data <- head(sorted_data, 20)
top_20_data <- top_20_data[order(top_20_data$vipVn, decreasing = FALSE), ]
# 将 Metabolite 列转换为因子，并设置顺序
top_20_data$metabolin <- factor(top_20_data$metabolin, levels = top_20_data$metabolin)

# 创建散点图
p <- ggplot(top_20_data, aes(x = vipVn, y = metabolin,color=types)) +
  geom_point() +  # 添加散点
  labs(x = "VIP Score", y = "Metabolite ID") +  # 设置坐标轴标签
  labs(title = paste0(titlename," VIP score Plot"))+scale_color_manual(values = c("#00AFBB","#FC4E07"))+
  guides(colour=guide_legend(title=titlename))+
  theme(
    axis.title.x = element_text(size = 15,margin = margin(t=10),colour = "black"),
    axis.title.y = element_text(size = 15,margin = margin(r=10),colour = "black"),
    axis.text.y = element_text(size = 13,colour = c('black')),
    axis.text.x  = element_text(size = 13,colour = c('black')),
    panel.background = element_blank(),
    plot.title = element_text(size = 18,colour = c('black'),vjust = 0.5,hjust = 0.5),
    panel.border = element_rect(color="black", size=1, linetype="solid",fill = NA))
ggsave(p,filename = output,width=8,height=6)
library(argparser, quietly=TRUE)
library(ggplot2)
library(ggrepel)
library(ggnewscale)
library(dplyr)

# Create a parser
p <- arg_parser("run Volcano Plot")

# Add command line arguments


p <- add_argument(p, "--allmetabolintbale", help="all_meta_result.csv",type="character")
p <- add_argument(p,"--output",help = "output file name",type = "character")
p <- add_argument(p,"--titlename",help = "title name",type = "character")

p <- add_argument(p,"--width",help = "width size")
p <- add_argument(p,"--height",help = "height size")
argv <- parse_args(p)


metatable <- argv$allmetabolintbale
output <- argv$output
width <- as.numeric(argv$width)
height <- as.numeric(argv$height)
titlename <- argv$titlename

meta_all <- read.table(metatable,header = TRUE,sep='\t')

# table(meta_all$types)
# meta_all$type2<-case_when(meta_all$types=="Up"~paste0("Up ",table(meta_all$types)[[3]]),
#                     meta_all$types=="NoSig"~paste0("NoSig ",table(meta_all$types)[[2]]),
#                     meta_all$types=="Down"~paste0("Down ",table(meta_all$types)[[1]]))


# 绘制不显著基因图层
nosig <- ggplot(meta_all,aes(x = log2fc,y = flog10_pvalue,size = vipVn,color=type2)) +
  # 不显著基因图层
  geom_point(data = meta_all %>% filter(types == 'NoSig' ),
             color = 'grey',alpha = .5) +
  # 修改颜色
  new_scale('color') +
  scale_x_continuous(limits = c(-ceiling(quantile(meta_all$log2fc,0.985)),ceiling(quantile(meta_all$log2fc,0.985)))) +
  scale_y_continuous(limits = c(0,ceiling(max(meta_all$flog10_pvalue))))+
  theme(
    axis.title.x = element_text(size = 15,margin = margin(t=10),colour = "black"),
    axis.title.y = element_text(size = 15,margin = margin(r=10),colour = "black"),
    axis.text.y = element_text(size = 13,colour = c('black')),
    axis.text.x  = element_text(size = 13,colour = c('black')),
    panel.background = element_blank(),
    plot.title = element_text(size = 18,colour = c('black'),vjust = 0.5,hjust = 0.5),
    panel.border = element_rect(color="black", size=1, linetype="solid",fill = NA))+
  # 添加x轴标签
  xlab(bquote(Log[2]*'(Fold Change)')) +
  # 添加y轴标签 
  ylab(bquote(-Log[10]*italic('P')*"value"))


# 绘制显著基因图层
sig <- nosig + 
  # 显著基因图层
  geom_point(data = meta_all %>% filter(types != 'NoSig'),
             # 点大小
             
             aes(color = type2),alpha = .8)+
  geom_hline(yintercept = -log10(0.05), linetype = "dashed", color = "black",alpha = .8)+
  geom_vline(xintercept = 1, linetype = "dashed", color = "black",alpha = .8)+
  geom_vline(xintercept = -1, linetype = "dashed", color = "black",alpha = .8)+
  scale_size_continuous(range = c(0.5, 4))+  # 控制点的大小
  guides(colour=guide_legend(title=titlename))+labs(title = titlename)+scale_color_manual(values = c("#00AFBB","#FC4E07"))
if (is.na(height)==1){
  height<-5
}else{
  height <- height
}
print(paste0("height this is ",height))
if (is.na(width)==1){
  width<-5
}else{
  width <- width
}
ggsave(sig,filename = output,width=width,height=height)

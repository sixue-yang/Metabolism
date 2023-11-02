rm(list = ls())
library(ggplot2)
library(dplyr)
library(argparser, quietly=TRUE)

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

# 筛选出 Up 和 Down 中 log2fc 绝对值最大的前 10 个行
top_10_up <- meta_all %>%
  filter(types == "Up") %>%
  arrange(desc(abs(log2fc))) %>%
  head(10)

top_10_down <- meta_all %>%
  filter(types == "Down") %>%
  arrange(desc(abs(log2fc))) %>%
  head(10)

top_10_combined <- bind_rows(top_10_up, top_10_down)

top_10_combined <- top_10_combined[order(top_10_combined$log2fc, decreasing = FALSE), ]
top_10_combined$metabolin <- factor(top_10_combined$metabolin, levels = top_10_combined$metabolin)

# 创建水平柱状图
p <- ggplot(top_10_combined, aes(x = log2fc, y = metabolin)) +
  geom_bar(stat = "identity", position = "identity", aes(fill = types), width = 0.7) +
  geom_text(aes(label = sprintf("%.2f", log2fc)), hjust = 0, size = 3)+
  scale_fill_manual(values = c("Up" = "#FC4E07", "Down" = "#00AFBB"))+
  theme(
    axis.title.x = element_text(size = 15,margin = margin(t=10),colour = "black"),
    axis.title.y = element_text(size = 15,margin = margin(r=10),colour = "black"),
    axis.text.y = element_text(size = 13,colour = c('black')),
    axis.text.x  = element_text(size = 13,colour = c('black')),
    panel.background = element_blank(),
    plot.title = element_text(size = 18,colour = c('black'),vjust = 0.5,hjust = 0.5),
    panel.border = element_rect(color="black", size=1, linetype="solid",fill = NA))+
  guides(fill = "none") +
  xlab(bquote(Log[2]*'(Fold Change)'))+
  ylab('Metabolite ID')
  #coord_flip()
ggsave(p,filename = output,width=8,height=6)
library(ggplot2)
library(argparser, quietly=TRUE)

p <- arg_parser("run Z-score of metabolin")
# Add command line arguments
p <- add_argument(p, "--zdata", help="plot z-score data",type="character")
p <- add_argument(p,"--output",help = "output file name",type = "character")
# Parse the command line arguments
argv <- parse_args(p)

data_p <- argv$zdata
output <- argv$output

data = read.table(data_p,header = TRUE,fileEncoding = "UTF-8")

unique_values = unique(data$metabolite)
num_unique_values = length(unique_values)



p = ggplot(data, aes(x = value, y = metabolite,color=Group)) +
  geom_point() +
  labs(x = "Z-score", y = "") +
  scale_fill_manual(values = c("#FC4E07", "#00AFBB")) +
  ggtitle("")+
  theme(
    axis.title.x = element_text(size = 15,margin = margin(t=10),colour = "black"),
    axis.title.y = element_text(size = 15,margin = margin(r=10),colour = "black"),
    axis.text.y = element_text(size = 8,colour = c('black')),
    axis.text.x  = element_text(size = 13,colour = c('black')),
    panel.background = element_blank(),
    plot.title = element_text(size = 18,colour = c('black'),vjust = 0.5,hjust = 0.5),
    panel.border = element_rect(color="black", size=1, linetype="solid",fill = NA),
    panel.grid.major.y = element_line(color = "gray", linetype = "dotted"),  # ��Ҫ������
    panel.grid.minor.y = element_line(color = "gray", linetype = "dotted"))  # ��Ҫ������

height = 20
width = 8
if (num_unique_values < 50) {
  height = num_unique_values/3  # 重新赋值为100（或者你想要的值）
  width = height * 0.5
}
ggsave(p,filename=output,height = height,width = width)

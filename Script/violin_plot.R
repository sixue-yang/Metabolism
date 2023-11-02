library(ggplot2)
library(argparser, quietly=TRUE)


p <- arg_parser("run violin of metabolin")
# Add command line arguments
p <- add_argument(p, "--violin", help="plot violin data",type="character")
p <- add_argument(p,"--output",help = "output file name",type = "character")
# Parse the command line arguments
argv <- parse_args(p)

data_p <- argv$violin
output <- argv$output
data = read.table(data_p,header = TRUE,fileEncoding = "UTF-8")

unique_values <- unique(data$metabolite)
num_unique_values <- length(unique_values)

# ��Ψһֵ���������Ų�ȡ��
sqrt_num_unique_values <- as.integer(sqrt(num_unique_values))

p = ggplot(data, aes(x = Group, y = value, fill = Group)) +
  geom_violin() +
  geom_boxplot(width = 0.1, fill = "white", color = "black") +  # ��������ͼ
  labs(x = "", y = "Normalized Intensity",title='Violin Plot of Normalized Values') +
  scale_fill_manual(values = c("#FC4E07", "#00AFBB")) +  # �Զ�����ɫ
  
  facet_wrap(~metabolite, scales = "free_y")  

p
ggsave(p,filename=output,height = sqrt_num_unique_values*2.2,width = sqrt_num_unique_values*2.2,limitsize = FALSE)

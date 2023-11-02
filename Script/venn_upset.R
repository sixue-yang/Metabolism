library(argparser, quietly=TRUE)
library(UpSetR)
library(ggplot2)


p <- arg_parser("run venn plot")

# Add command line arguments
p <- add_argument(p, "--venn", help="venn.data",type="character")
p <- add_argument(p,"--output",help = "output file name",type = "character")
#p <- add_argument(p,"--width",help = "width size")
#p <- add_argument(p,"--height",help = "height size")
# Parse the command line arguments
argv <- parse_args(p)


venndata_path <- argv$venn
output <- argv$output
#width <- as.numeric(argv$width)
#height <- as.numeric(argv$height)


venn_data = read.table(venndata_path,header = TRUE,sep = "\t",quote = "",fileEncoding = "UTF-8",row.names = 1)
#width = 60 * 15
#height = ncol(venn_data) * 120
pdf(output,width = 8, height = 5,onefile = FALSE)
upset(venn_data,nsets = ncol(venn_data),nintersects=60,main.bar.color = "black", sets.bar.color = "yellow",order.by='freq',decreasing = T)
dev.off() 
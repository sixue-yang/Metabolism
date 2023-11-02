library(argparser, quietly=TRUE)
library(dplyr)
library(ggplot2)


p <- arg_parser("run enrichment analysis")

# Add command line arguments
p <- add_argument(p, "--keggannotation", help="keggannotation.csv",type="character")
p <- add_argument(p, "--diffkeggid", help="diff_keggid.txt(enrichment)", type="character")
p <- add_argument(p,"--number",help = "number of max terms",type = "character")
p <- add_argument(p,"--output_result",help = "output result name",type = "character")
p <- add_argument(p,"--output_cnetplot",help = "output cnetplot name",type = "character")
p <- add_argument(p,"--output_barplot",help = "output barplot name",type = "character")
p <- add_argument(p,"--output_dotplot",help = "output dotplot name",type = "character")
p <- add_argument(p,"--width",help = "width size")
p <- add_argument(p,"--height",help = "height size")
# Parse the command line arguments
argv <- parse_args(p)

keggannotation <- argv$keggannotation
diffkeggid <- argv$diffkeggid
number <- as.numeric(argv$number)
output_result <- argv$output_result
output_cnetplot <- argv$output_cnetplot
output_barplot <- argv$output_barplot
output_dotplot <- argv$output_dotplot
width <- as.numeric(argv$width)
height <- as.numeric(argv$height)


#keggannotation <- read.csv("total_compound3.csv")
keggannotation <- read.table(keggannotation,header = TRUE,sep = "\t",quote = "",fileEncoding = "UTF-8")
# dim(keggannotation)
diff <- read.csv(diffkeggid)
if (nrow(diff) == 0) {
  cat("", file = output_result)
  pdf(output_cnetplot)
  dev.off()
  pdf(output_barplot)
  dev.off()
  pdf(output_dotplot)
  dev.off()
} else {
  total<-keggannotation[,c(3,1)]
  x<-clusterProfiler::enricher(gene = diff$ID,TERM2GENE = total,minGSSize = 1,pvalueCutoff = 1,qvalueCutoff = 1)
  write.table(as.data.frame(x@result),paste0(output_result),sep='\t',row.names=FALSE)
  p1<-clusterProfiler::cnetplot(x,circular=TRUE)
  p2<-barplot(x,showCategory = number,color = "pvalue")
  p3<- enrichplot::dotplot(x,showCategory = number,color = "pvalue")

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
  print(paste0("width this is ",width))
  ggsave(p1,filename = paste0(output_cnetplot),width=width,height=width)
  ggsave(p2,filename = paste0(output_barplot),width=width,height=height)
  ggsave(p3,filename = paste0(output_dotplot),width=width,height=height)
}



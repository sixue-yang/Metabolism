rm(list = ls())
library(tidyr)
library(ggplot2)
if(!require(ropls)) BiocManager::install('ropls')
#加载
library(ropls)
library(argparser, quietly=TRUE)

# 需要输出
# 文件1 1、p-value 2、q-value 3、FC 4、log2 FC 5 vip

# Create a parser
p <- arg_parser("run different metabolin analysis")
p <- add_argument(p, "--adjust", help = "adjust methods: fdr, none, holm, hochberg, hommel, bonferroni", type = "character")
p <- add_argument(p, "--metabolintable", help = "metabolin_result", type = "character")
p <- add_argument(p, "--treatname", help = "treat name (must match the group column)", type = "character")
p <- add_argument(p, "--controlname", help = "control name (must match the group column)", type = "character")
p <- add_argument(p, "--output", help = "output file name prefix", type = "character")

argv <- parse_args(p)

adjust <- argv$adjust
metatable <- argv$metabolintable
output <- argv$output
treat <- argv$treatname
control <- argv$controlname

# 读取差异组代谢表达数据
meta_all <- read.table(metatable,header = TRUE,row.names = 1)
group_list = meta_all$Group
meta <- meta_all[, !(names(meta_all) %in% c("Group"))]
lv <- as.factor(group_list)
levels(lv)<-c(treat,control)
# 差异分析，两组代谢物 t检验
# perform_t_test <- function(x, col_name) {
#   cat("Performing t-test for column:", col_name, "\n")
#   result <- t.test(x ~ lv)
#   cat("p-value:", result$p.value, "\n")
#   cat("q-value:", p.adjust(result$p.value, method = adjust), "\n")
#   cat("\n")
#   return(result)
# }

# # 对每列数据执行 t 检验
# res <- lapply(colnames(meta), function(col_name) {
#   perform_t_test(meta[[col_name]], col_name)
# })
res <- apply(meta,2,function(x){t.test(x~lv)})
pvalue <- sapply(res,function(x) x$p.value)
qvalue <- p.adjust(pvalue,method = adjust)
fc <- sapply(res,function(x) as.data.frame(x$estimate)[1,]/as.data.frame(x$estimate)[2,])
expr <- data.frame(metabolin = rownames(t(meta)))
rownames(expr) =  rownames(t(meta))
expr$pvalue<-pvalue
expr$qvalue<-qvalue
expr$fc<-fc
expr$log2fc<-log2(fc)

# OPLS-DA 分析
set.seed(1234)

# tryCatch({
#   oplsda <- opls(x = meta, y = group_list, predI = 1, orthoI = NA, fig.pdfC = paste0(output, "_oplsda.pdf"))
#   vipVn <- getVipVn(oplsda)
#   vipVn_select <- cbind(expr[names(vipVn),], vipVn)
# }, error = function(e) {
#   cat("An error occurred:", conditionMessage(e), "\n")
#   expr$vipVn <- rep(0, nrow(meta))  # 将vip列全部赋值为0
#   vipVn_select <- expr
# })
oplsda <- opls(x = meta, y = group_list, predI = 5, orthoI = 0, crossvalI=nrow(meta)-1,fig.pdfC = paste0(output, "_oplsda.pdf"))
vipVn <- getVipVn(oplsda)
vipVn_select <- cbind(expr[names(vipVn),], vipVn)

# oplsda <- opls(x = meta, y = group_list,predI = 1, orthoI = NA, fig.pdfC=paste0(output,"oplsda.pdf"))

# vipVn <- getVipVn(oplsda)

write.table(as.data.frame(vipVn_select),paste0(output,"_Diff_count.xls"),row.names = FALSE,quote=FALSE,sep='\t')



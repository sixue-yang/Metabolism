rm(list = ls())
library(FactoMineR)
library(scatterplot3d)
library(factoextra)
library(ggplot2)
library(ggforce)
library(mixOmics)
library(argparser, quietly=TRUE)

p <- arg_parser("run PCA and PLS-DA plot of metabolin")

# Add command line arguments

p <- add_argument(p, "--metabolintbale", help="clean_matrix.csv",type="character")
p <- add_argument(p,"--outpca2d",help = "output pca2d path",type="character")
p <- add_argument(p,"--outpca3d",help = "output pca3d path",type = "character")
p <- add_argument(p,"--outplsda",help = "output plsda path",type = "character")

# Parse the command line arguments
argv <- parse_args(p)

metatable <- argv$metabolintbale
out_pca2d = argv$outpca2d
out_pca3d = argv$outpca3d
out_plsda = argv$outplsda

meta_all <- read.table(metatable,header = TRUE,row.names = 1)
group_list = meta_all$Group
meta <- meta_all[, !(names(meta_all) %in% c("Group"))]
ncomp = 2


# 颜色设置
num_categories <- length(unique(group_list))
color_palette <- scales::hue_pal()(num_categories)
color_mapping <- setNames(color_palette, sort(unique(group_list)))
col_vector <- color_palette[match(group_list, names(color_mapping))]


#### PLS-DA Plot ####
plsda <- mixOmics::plsda(meta, as.factor(group_list), ncomp = ncomp)
mixOmics::plotIndiv(plsda, ind.names = TRUE, ellipse = TRUE, legend = TRUE)
a <- unclass(plsda)
dataplsda <- as.data.frame(a$variates$X)
dataplsda$SampleType = group_list
eig = round(a[[17]]$X,4)
p <- ggplot(data = dataplsda,aes(x=comp1,y=comp2,color=group_list))+geom_point(size=2)+
  stat_ellipse(aes(fill = factor(group_list)), linetype = 2)+
  labs(x=paste("T score 1 (", format(100 * eig[1]), "%)", sep=""),
       y=paste("T score 2 (", format(100 * eig[2] ), "%)", sep=""))+theme_test()+
  labs(title = "PLS-DA") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5),panel.border = element_rect(color = "black", fill = NA))+
  guides(color=guide_legend(title = NULL),shape=guide_legend(title = NULL))
# output="test5"
ggsave(plot = p,filename = out_plsda,width = 8,height = 6)

#### PCA 2D Plot ####
dat.pca <- prcomp(meta)

contributions <- dat.pca$sdev^2 / sum(dat.pca$sdev^2) * 100
contributions <- round(contributions, 2)  # 保留两位小数
pca_2d = fviz_pca_ind(dat.pca,ind="point",col.ind=group_list,legend.title="Groups",addEllipses = T) + theme_minimal() + 
  theme(panel.border = element_rect(color = "black", fill = NA)) + 
  labs(
    x = paste("PC1 (", contributions[1], "%)", sep = ""),
    y = paste("PC2 (", contributions[2], "%)", sep = ""),
    title = "PCA Scatter Plot"
  )

#pca_2d <- pca_2d + scale_fill_manual(values = color_palette, labels = unique(group_list))
ggsave(plot = pca_2d,filename = out_pca2d,width = 8,height = 6)


#### PCA 3D plot ####
pdf(out_pca3d,h=8,w=10)
scatterplot3d(dat.pca$x[, 1], dat.pca$x[, 2], dat.pca$x[, 3],xlab="PC1", ylab="PC3",zlab="PC2",color=col_vector,pch=19,cex.symbols=1.5,mar=c(3,3,3,10)+0.1)
legend("right", legend=sort(unique(group_list)),pch=19, col=color_palette,bty="n",ncol=1)
dev.off()
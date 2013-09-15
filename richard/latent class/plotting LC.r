library(RMySQL)
library(ggplot2)
library(reshape2)

sqluser = ""
sqlpass = ""
con = dbConnect(drv,host="localhost",dbname="git",user=sqluser,pass=sqlpass)

setwd("C:\\Dropbox\\rmills\\Postdoc\\latent class")

classes = read.csv("18-classes.csv", stringsAsFactors = FALSE)

attach(classes)
df = data.frame(Cluster, PushEvents, WatchEvents, IssuesEvents, ForkEvents, PullRequestEvents, DeleteEvents)

melted = melt(df)

melted$Cluster = as.character(melted$Cluster)
melted$Cluster[melted$Cluster == "Cluster1"] = "Cluster1 - 41%"
melted$Cluster[melted$Cluster == "Cluster2"] = "Cluster2 - 17%"
melted$Cluster[melted$Cluster == "Cluster3"] = "Cluster3 - 16%"
melted$Cluster[melted$Cluster == "Cluster4"] = "Cluster4 - 7%"
melted$Cluster[melted$Cluster == "Cluster5"] = "Cluster5 - 5%"
melted$Cluster[melted$Cluster == "Cluster6"] = "Cluster6 - 4%"
melted$Cluster[melted$Cluster == "Cluster7"] = "Cluster7 - 3%"
melted$Cluster[melted$Cluster == "Cluster8"] = "Cluster8 - 2%"
melted$Cluster[melted$Cluster == "Cluster9"] = "Cluster9 - 1%"
melted$Cluster[melted$Cluster == "Cluster10"] = "Cluster10 - 1%"
melted$Cluster[melted$Cluster == "Cluster11"] = "Cluster11 - 0.5%"
melted$Cluster[melted$Cluster == "Cluster12"] = "Cluster12 - 0.5%"
melted$Cluster[melted$Cluster == "Cluster13"] = "Cluster13 - 0.2%"
melted$Cluster[melted$Cluster == "Cluster14"] = "Cluster14 - 0.1%"
melted$Cluster[melted$Cluster == "Cluster15"] = "Cluster15 - 0.1%"
melted$Cluster[melted$Cluster == "Cluster16"] = "Cluster16 - 0.1%"
melted$Cluster[melted$Cluster == "Cluster17"] = "Cluster17 - 0.001%"
melted$Cluster[melted$Cluster == "Cluster18"] = "Cluster18 - 0.001%"


melted$Cluster = factor(melted$Cluster, levels = c("Cluster1 - 41%", "Cluster2 - 17%", "Cluster3 - 16%", "Cluster4 - 7%", "Cluster5 - 5%", "Cluster6 - 4%", "Cluster7 - 3%", "Cluster8 - 2%",
														"Cluster9 - 1%", "Cluster10 - 1%", "Cluster11 - 0.5%", "Cluster12 - 0.5%", "Cluster13 - 0.2%", "Cluster14 - 0.1%", "Cluster15 - 0.1%", "Cluster16 - 0.1%", "Cluster17 - 0.001%", "Cluster18 - 0.001%"))

p.events = 	
	ggplot(melted) +
	geom_bar(aes(x = variable, y = value, fill = variable)) +
	facet_wrap(~Cluster, scales = "free", ncol = 3) +
	scale_fill_brewer(type="seq", palette="Set1") +
	opts(axis.text.x = theme_text( vjust = 1, size = 8))
	

	
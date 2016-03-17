library(RMySQL)
library(ggplot2)
library(slam)
library(tm)
library(RTextTools)
library(topicmodels)
library(reshape2)
library(irr)

setwd("C:/git/data/")

adrian = read.csv("orgs_manual_coding_sample_am.csv", stringsAsFactors = FALSE)
richard = read.csv("orgs_manual_coding_sample_richard.csv", stringsAsFactors = FALSE)

k = kappa2(cbind(adrian$organisation.type, richard$type))
#0.45, not great

richard$am = adrian$organisation.type

richard$match = 0
richard$match[richard$type == richard$am] = 1



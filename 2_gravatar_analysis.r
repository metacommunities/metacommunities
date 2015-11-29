library(bigrquery)
library(RCurl)
library(png)
library(jpeg)

prj = 'metacommunities'

query  = "SELECT repository_url, payload_member_avatar_url FROM [githubarchive:github.timeline] where payload_member_avatar_url != '' LIMIT 1000"

res =query_exec(query, project = prj)
colnames(res) = c('repo_url', 'avatar_url')
avatar_urls = unique(res$avatar_url)

save_avatar <- function(url){
    im = getURLContent(url)
    #writePNG(im,file(paste(url, '.png', sep='')))
}

imgs = sapply(avatar_urls[1:5], save_avatar)

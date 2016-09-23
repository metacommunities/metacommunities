    library(bigrquery)
    library(ggplot2)
    library(readr)
    library(dplyr)


    construct_query <- function(query_term) {
        query_full = gsub(pattern='\\n', replacement =' ', x=paste("SELECT
        repo.name,
        created_at,
        COUNT(type) AS cnt
        FROM
        [githubarchive:year.2011],
        [githubarchive:year.2012],
        [githubarchive:year.2013],
        [githubarchive:year.2014],
        [githubarchive:year.2015],
        TABLE_DATE_RANGE([githubarchive:day.], TIMESTAMP('2016-01-01'), TIMESTAMP('2016-06-31'))
        WHERE
        type= 'ForkEvent'
        AND LOWER(repo.name) CONTAINS('",
        query_term,
        "')
        GROUP BY
        repo.name,
        created_at,
        ORDER BY
        created_at,
        cnt DESC", sep=''))
        return(query_full)
    }
    

    fetch_data <- function(query_term, pages_to_fetch=4, force_refresh=FALSE) {
        query_full = construct_query(query_term)
        file = paste('data/', query_term, '_forks.csv',sep='')
        if (file.exists(file) && force_refresh == FALSE) {
            df_and = read_csv(file)
        } else {
            df_and = query_exec('metacommunities', query= query_full, max_pages= pages_to_fetch )
            write_csv(path=file, x= df_and)
        }
        head(df_and)
        nrow(df_and)
        return(df_and)
    }


    plot_forks <- function(df_and, query_term, fork_count_cutoff, binwidth, without_query = FALSE){
        top_forks = df_and %>%group_by(repo_name) %>% summarise(evt_cnt = n()) %>% filter(evt_cnt>fork_count_cutoff) %>% arrange(desc(evt_cnt))
        nrow(top_forks)
        if (without_query){
            to_plot= df_and[df_and$repo_name %in% top_forks$repo_name[-1], ]
        } else {
            to_plot = df_and[df_and$repo_name %in% top_forks$repo_name, ]
        }
        nrow(to_plot)
        binw = binwidth
        g = ggplot(to_plot, aes(x=as.Date(created_at),   fill=repo_name)) + geom_line(aes(y = ..count..),  color='black',size=0.2, alpha=0.3,  stat = "bin",position='stack', binwidth=binw) +  theme(legend.position='blank') + geom_area(aes(y = ..count..), stat='bin',alpha=0.4,  binwidth=binw)  + scale_colour_brewer(type='div', palette='RdYlGn') + ylab('Fork counts') + xlab('Date of Fork')

        if (without_query){
            g + ggtitle(paste('Forks associated with the name `', query_term, '` alone', sep=''))
            } else {
            g +  ggtitle(paste('Forks associated with the name `', query_term, '`', sep=''))
            }
    }

    query_term = 'android'
    fork_count_cutoff = 50
    binwidth=10 
    pages_to_fetch= Inf
    df_and = fetch_data(query_term, Inf, TRUE)
    plot_forks(df_and, query_term, fork_count_cutoff, binwidth, FALSE)

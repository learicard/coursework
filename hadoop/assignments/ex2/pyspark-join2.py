#!/usr/bin/env python

def split_show_views(line):
    show = line.split(',')[0]
    views = line.split(',')[1]
    return(show, views)

def split_show_channel(line):
    show = line.split(',')[0]
    channel = line.split(',')[1]
    return(show, channel)

def extract_channel_views(line):
    line = line[1]
    channel = line[1]
    views = line[0]
    return(channel, int(views))    

show_view_file = sc.textFile("input/join2_gennum?.txt")
show_views = show_view_file.map(split_show_views)

show_channel_file = sc.textFile("input/join2_genchan?.txt")
show_channel = show_channel_file.map(split_show_channel)

# join datasets
joined_dataset = show_views.join(show_channel)
channel_views = joined_dataset.map(extract_channel_views)

# sum total number of viewers per channel 
channel_views.groupByKey().mapValues(sum).collect()


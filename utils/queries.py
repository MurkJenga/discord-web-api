queries = {
    "insert_message": 'INSERT INTO message (channel_id, guild_id, message_id, created_dtm, content_txt, og_content_txt, author_id) VALUES (%s, %s, %s, %s, %s, %s, %s)',
    "update_message": 'UPDATE message SET last_modified_dtm = %s, content_txt = %s WHERE message_id = %s',
    "delete_message": 'UPDATE message SET is_active = 0 WHERE message_id = %s',
    "insert_emoji": 'INSERT INTO reaction (user_id, message_id, emoji_txt, emoji_id, channel_id, guild_id, added_dtm) VALUES (%s, %s, %s, %s, %s, %s, %s)',
    "delete_emoji": 'UPDATE reaction SET removed_dtm = %s, is_active = 0 WHERE message_id = %s and user_id = %s and emoji_txt = %s',
    "given_query": """
                    select 
                    concat(
                        ROW_NUMBER() OVER ( ORDER BY count(u.username) desc ), ". ",
                        u.username, ": ",
                        count(*) 
                        ) stats,
                    u.username,
                    r.emoji_txt,
                    r.emoji_id,
                    coalesce(concat("<", ":", r.emoji_txt, ":", emoji_id, ">"), r.emoji_txt) emoji_identifier,
                    count(*) recieved
                    from user u
                    join reaction r on r.user_id = u.user_id
                    where  coalesce(concat("<", ":", r.emoji_txt, ":", emoji_id, ">"), r.emoji_txt) = %s
                    group by u.username, r.emoji_txt, r.emoji_id""",
    "recieved_query": """
                    select 
                    concat(
                        ROW_NUMBER() OVER ( ORDER BY count(u.username) desc ), ". ",
                        u.username, ": ",
                        count(*) 
                        ) stats,
                    u.username,
                    r.emoji_txt,
                    r.emoji_id,
                    coalesce(concat("<", ":", r.emoji_txt, ":", emoji_id, ">"), r.emoji_txt) emoji_identifier,
                    count(*) recieved
                    from user u
                    join message m on u.user_id = m.author_id
                    join reaction r on r.message_id = m.message_id
                    where  coalesce(concat("<", ":", r.emoji_txt, ":", emoji_id, ">"), r.emoji_txt) = %s
                    group by u.username, r.emoji_txt, r.emoji_id""",
    "whogave_query": """
                    select 
                    concat(
                        ROW_NUMBER() OVER ( ORDER BY count(m.message_id) desc ), ". ",
                        reactedUser.username, ": ",
                        format(count(m.message_id), 0)
                        ) stats,
                    reactedUser.username,
                    count(*)
                    from user u
                    join message m on m.author_id = u.user_id
                    join reaction r on r.message_id = m.message_id
                    join user reactedUser on reactedUser.user_id = r.user_id
                    where
                    (coalesce(concat("<", ":", r.emoji_txt, ":", emoji_id, ">"), r.emoji_txt)) = %s
                    and u.user_id = %s
                    group by 2""",
    "whorecieved_query": """
                    select 
                        concat(
                        ROW_NUMBER() OVER ( ORDER BY count(m.message_id) desc ), ". ",
                        author.username, ": ",
                        format(count(m.message_id), 0)
                        ) stats, 
                        r.emoji_txt,
                        author.username as author,
                        count(*) as reactions
                    from user u
                    join reaction r on u.user_id = r.user_id
                    join message m on m.message_id = r.message_id
                    join user author on author.user_id = m.author_id
                    where
                        coalesce(concat("<", ":", r.emoji_txt, ":", emoji_id, ">"), r.emoji_txt) = %s
                        and u.user_id = %s
                    group by 
                        u.username,
                        r.emoji_txt,
                        author.username""",
    "total_query": """
                    select concat(
                        ROW_NUMBER() OVER ( ORDER BY count(m.message_id) desc ), ". ",
                        u.username, ": ",
                        format(count(m.message_id), 0)
                        ) stats
                        ,count(*) as total
                    from user u 
                    left join message m on m.author_id = u.user_id and date(created_dtm) <= COALESCE(%s, current_date())
                    where u.isBot = 0 
                    group by u.username
                    order by 2 desc""", 
    "botrequest_query": "INSERT INTO request (type, request_txt, request_dte) VALUES ( %s, %s, %s)",
    "last30_query": """
                    with last30Messages as (
                    select * from message where datediff(current_date, created_dtm)  <  31),
                    totalMessages as (
                        select count(*) totalMsgs, u.user_id
                        from user u
                        join last30Messages m on m.author_id = u.user_id
                        group by u.user_id),
                    last30Reactions as (
                    select * from reaction where datediff(current_date, added_dtm)  <  31),
                    avgWordsMsg as (
                        select 
                            sum((length(m.content_txt) - length(replace(m.content_txt,' ',''))) + 1) /count(m.message_id) as averageWrds,
                            u.user_id
                        from user u
                        join last30Messages m on m.author_id = u.user_id
                        group by u.user_id	
                        ),
                    lastMessage as (
                        select 
                            max(date(m.created_dtm)) as lastMsg,
                            u.user_id
                        from user u
                        join message m on m.author_id = u.user_id
                        group by 2
                        ),
                    totalWrds as ( 
                        select 
                            sum((length(m.content_txt) - length(replace(m.content_txt,' ',''))) + 1) totalWrds,
                            u.user_id
                        from user u
                        join last30Messages m on m.author_id = u.user_id
                        group by u.user_id	 
                        ),
                    avgPerDay as (
                        select 
                            count(m.message_id) / 30 as avgPerDay,
                            u.user_id
                        from user u
                        join last30Messages m on m.author_id = u.user_id
                        group by u.user_id	 
                        ),
                    reactionGiven as (
                        select 
                            u.user_id,
                            count(*) as reactGiv
                        from user u 
                        join last30Reactions r on r.user_id = u.user_id and is_active = 1
                        group by 1
                        ),
                    reactionRec as (
                        select 
                            count(emoji_txt) reactRec,
                            u.user_id
                        from user u
                        join last30Messages m on m.author_id = u.user_id
                        join last30Reactions r on r.message_id = m.message_id and r.user_id != m.author_id
                        group by 2
                        ),
                    topReact as (
                        select 
                            u.user_id,
                            (coalesce(concat("<", ":", r.emoji_txt, ":", emoji_id, ">"), r.emoji_txt) ) as topReact,
                            count(*),
                            ROW_NUMBER() OVER ( partition by u.user_id ORDER BY count(*) desc ) rowno
                        from user u
                        join last30Reactions r on r.user_id = u.user_id 
                        group by 1, 2
                        )
                        
                    select 
                        u.user_id,
                        username,
                        coalesce(DATE_FORMAT(join_dtm, '%m-%d-%Y'), 'N/A'  ) joinDate,
                        coalesce(totMsgs.totalMsgs, 0) totalMsgs,
                        round(coalesce(averageWrds, 0),0) averageWrds,
                        coalesce(DATE_FORMAT(lastMsg.lastMsg, '%m-%d-%Y'), 'N/A') lastMsg,
                        coalesce(totWrds.totalWrds, 0) totalWrds,
                        round(coalesce(perDay.avgPerDay, 0),0) avgPerDay,
                        coalesce(rGiv.reactGiv, 0) reactGiv,
                        coalesce(reactRec, 0) reactRec,
                        coalesce(tReact.topReact, 'N/A') as topReact
                    from user u
                    left join totalMessages totMsgs on totMsgs.user_id = u.user_id
                    left join avgWordsMsg averg on averg.user_id = u.user_id
                    left join lastMessage lastMsg on lastMsg.user_id = u.user_id
                    left join totalWrds totWrds on totWrds.user_id = u.user_id
                    left join avgPerDay perDay on perDay.user_id = u.user_id
                    left join reactionGiven rGiv on rGiv.user_id = u.user_id 
                    left join reactionRec rRec on rRec.user_id = u.user_id
                    left join topReact tReact on tReact.user_id = u.user_id AND rowno = 1
                    where 
                        u.user_id = %s """,
    "user_query": """
                    with totalMessages as (
                    select count(*) totalMsgs, u.user_id
                    from user u
                    join message m on m.author_id = u.user_id
                    group by u.user_id),
                avgWordsMsg as (
                    select 
                        sum((length(m.content_txt) - length(replace(m.content_txt,' ',''))) + 1) /count(m.message_id) as averageWrds,
                        u.user_id
                    from user u
                    join message m on m.author_id = u.user_id
                    group by u.user_id	
                    ),
                lastMessage as (
                    select 
                        max(date(m.created_dtm)) as lastMsg,
                        u.user_id
                    from user u
                    join message m on m.author_id = u.user_id
                    group by 2
                    ),
                totalWrds as ( 
                    select 
                        sum((length(m.content_txt) - length(replace(m.content_txt,' ',''))) + 1) totalWrds,
                        u.user_id
                    from user u
                    join message m on m.author_id = u.user_id
                    group by u.user_id	 
                    ),
                avgPerDay as (
                    select 
                        count(m.message_id) / datediff(current_date(), date(u.join_dtm)) as avgPerDay,
                        u.user_id
                    from user u
                    join message m on m.author_id = u.user_id
                    group by u.user_id	 
                    ),
                reactionGiven as (
                    select 
                        u.user_id,
                        count(*) as reactGiv
                    from user u 
                    join reaction r on r.user_id = u.user_id and is_active = 1
                    group by 1
                    ),
                reactionRec as (
                    select 
                        count(emoji_txt) reactRec,
                        u.user_id
                    from user u
                    join message m on m.author_id = u.user_id
                    join reaction r on r.message_id = m.message_id and r.user_id != m.author_id
                    group by 2
                    ),
                topReact as (
                    select 
                        u.user_id,
                        (coalesce(concat("<", ":", r.emoji_txt, ":", emoji_id, ">"), r.emoji_txt) ) as topReact,
                        count(*),
                        ROW_NUMBER() OVER ( partition by u.user_id ORDER BY count(*) desc ) rowno
                    from user u
                    join reaction r on r.user_id = u.user_id 
                    group by 1, 2
                    )
                    
                select 
                    u.user_id,
                    username,
                    coalesce(DATE_FORMAT(join_dtm, "%m-%d-%Y"), 'N/A'  ) joinDate,
                    coalesce(totMsgs.totalMsgs, 0) totalMsgs,
                    round(coalesce(averageWrds, 0),0) averageWrds,
                    coalesce(DATE_FORMAT(lastMsg.lastMsg, "%m-%d-%Y"), 'N/A') lastMsg,
                    coalesce(totWrds.totalWrds, 0) totalWrds,
                    round(coalesce(perDay.avgPerDay, 0),0) avgPerDay,
                    coalesce(rGiv.reactGiv, 0) reactGiv,
                    coalesce(reactRec, 0) reactRec,
                    tReact.topReact
                from user u
                left join totalMessages totMsgs on totMsgs.user_id = u.user_id
                left join avgWordsMsg averg on averg.user_id = u.user_id
                left join lastMessage lastMsg on lastMsg.user_id = u.user_id
                left join totalWrds totWrds on totWrds.user_id = u.user_id
                left join avgPerDay perDay on perDay.user_id = u.user_id
                left join reactionGiven rGiv on rGiv.user_id = u.user_id 
                left join reactionRec rRec on rRec.user_id = u.user_id
                left join topReact tReact on tReact.user_id = u.user_id AND rowno = 1
                where 
                    u.user_id = %s """

                }
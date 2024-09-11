queries = {
    "insert_message": 'INSERT INTO message (channel_id, guild_id, message_id, created_dtm, content_txt, og_content_txt, author_id) VALUES (%s, %s, %s, %s, %s, %s, %s)',
    "update_message": 'UPDATE message SET last_modified_dtm = %s, content_txt = %s WHERE message_id = %s',
    "delete_message": 'UPDATE message SET is_active = 0 WHERE message_id = %s',
    "insert_emoji": 'INSERT INTO reaction (user_id, message_id, emoji_txt, emoji_id, channel_id, guild_id, added_dtm) VALUES (%s, %s, %s, %s, %s, %s, %s)',
    "delete_emoji": 'UPDATE reaction SET removed_dtm = %s, is_active = 0 WHERE message_id = %s and user_id = %s and emoji_txt = %s',
    "given_query": """select 
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
                    group by u.username, r.emoji_txt, r.emoji_id"""
}
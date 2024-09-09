queries = {
    "insert_query": 'INSERT INTO message (channel_id, guild_id, message_id, created_dtm, content_txt, og_content_txt, author_id) VALUES (%s, %s, %s, %s, %s, %s, %s)',
    "select_query": 'select * message limit 5'
}
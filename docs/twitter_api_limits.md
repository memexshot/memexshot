Resource / Endpoint	Pro Limit 	Basic Limit 	Free Limit 	Special Attributes
Tweets
DELETE /2/tweets/:id	50 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	17 requests / 24 hours
PER USER
17 requests / 24 hours
PER APP	
DELETE /2/users/:id/likes/:tweet_id	50 requests / 15 mins
PER USER	100 requests / 24 hours
PER USER	1 requests / 15 mins
PER USER	
DELETE /2/users/:id/retweets/:tweet_id	50 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
GET /2/tweets	900 requests / 15 mins
PER USER
450 requests / 15 mins
PER APP	15 requests / 15 mins
PER USER
15 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/tweets/:id	900 requests / 15 mins
PER USER
450 requests / 15 mins
PER APP	15 requests / 15 mins
PER USER
15 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/tweets/:id/liking_users	75 requests / 15 mins
PER USER
75 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
25 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/tweets/:id/quote_tweets	75 requests / 15 mins
PER USER
75 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
5 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/tweets/:id/retweeted_by	75 requests / 15 mins
PER USER
75 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
5 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/tweets/counts/all	300 requests / 15 mins
PER APP	
enhanced operators
1024 query length
GET /2/tweets/counts/recent	300 requests / 15 mins
PER APP	5 requests / 15 mins
PER APP	1 requests / 15 mins
PER APP	
512 query length
core operators
GET /2/tweets/search/all	1 requests / second
PER USER
1 requests / second
PER APP	
500 results per response
10 default results per response
enhanced operators
1024 query length
GET /2/tweets/search/recent	300 requests / 15 mins
PER USER
450 requests / 15 mins
PER APP	60 requests / 15 mins
PER USER
60 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
10 default results per response
100 results per response
512 query length
core operators
GET /2/tweets/search/stream	50 requests / 15 mins
PER APP	
1000 rules
does not support backfill
1024 rule length
enterprise
1 connection
250 Tweets per second
GET /2/tweets/search/stream/rules	450 requests / 15 mins
PER APP	
1000 rules
does not support backfill
1024 rule length
enterprise
1 connection
250 Tweets per second
GET /2/users/:id/liked_tweets	75 requests / 15 mins
PER USER
75 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
5 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/users/:id/mentions	300 requests / 15 mins
PER USER
450 requests / 15 mins
PER APP	10 requests / 15 mins
PER USER
15 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/users/:id/timelines/reverse_chronological	180 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
GET /2/users/:id/tweets	900 requests / 15 mins
PER USER
1500 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
10 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/users/reposts_of_me	75 requests / 15 mins
PER USER	75 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
100 results per response
POST /2/tweets	100 requests / 15 mins
PER USER
10000 requests / 24 hours
PER APP	100 requests / 24 hours
PER USER
1667 requests / 24 hours
PER APP	17 requests / 24 hours
PER USER
17 requests / 24 hours
PER APP	
POST /2/tweets/search/stream/rules	100 requests / 15 mins
PER APP	
1000 rules
does not support backfill
1024 rule length
enterprise
1 connection
250 Tweets per second
POST /2/users/:id/likes	1000 requests / 24 hours
PER USER	200 requests / 24 hours
PER USER	1 requests / 15 mins
PER USER	
POST /2/users/:id/retweets	50 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
PUT /2/tweets/:tweet_id/hidden	50 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
Users
DELETE /2/users/:source_user_id/following/:target_user_id	50 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
DELETE /2/users/:source_user_id/muting/:target_user_id	50 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
GET /2/users	900 requests / 15 mins
PER USER
300 requests / 15 mins
PER APP	100 requests / 24 hours
PER USER
500 requests / 24 hours
PER APP	1 requests / 24 hours
PER USER
1 requests / 24 hours
PER APP	
GET /2/users/:id	900 requests / 15 mins
PER USER
300 requests / 15 mins
PER APP	100 requests / 24 hours
PER USER
500 requests / 24 hours
PER APP	1 requests / 24 hours
PER USER
1 requests / 24 hours
PER APP	
GET /2/users/:id/blocking	15 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
GET /2/users/:id/muting	15 requests / 15 mins
PER USER	100 requests / 24 hours
PER USER	1 requests / 24 hours
PER USER	
GET /2/users/by	900 requests / 15 mins
PER USER
300 requests / 15 mins
PER APP	100 requests / 24 hours
PER USER
500 requests / 24 hours
PER APP	1 requests / 24 hours
PER USER
1 requests / 24 hours
PER APP	
GET /2/users/by/username/:username	900 requests / 15 mins
PER USER
300 requests / 15 mins
PER APP	100 requests / 24 hours
PER USER
500 requests / 24 hours
PER APP	3 requests / 15 mins
PER USER
3 requests / 15 mins
PER APP	
GET /2/users/me	75 requests / 15 mins
PER USER	250 requests / 24 hours
PER USER	25 requests / 24 hours
PER USER	
GET /2/users/search	900 requests / 15 mins
PER USER
300 requests / 15 mins
PER APP	
POST /2/users/:id/following	50 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
POST /2/users/:id/muting	50 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
Spaces
GET /2/spaces	300 requests / 15 mins
PER USER
300 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
25 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/spaces/:id	300 requests / 15 mins
PER USER
300 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
25 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/spaces/:id/buyers	300 requests / 15 mins
PER USER
300 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
25 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/spaces/:id/tweets	300 requests / 15 mins
PER USER
300 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
25 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/spaces/by/creator_ids	300 requests / 15 mins
PER USER
1 requests / second
PER APP	5 requests / 15 mins
PER USER
25 requests / second
PER APP	1 requests / second
PER USER
1 requests / 15 mins
PER APP	
GET /2/spaces/search	300 requests / 15 mins
PER USER
300 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
25 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
Direct Messages
DELETE /2/dm_events/:id	1500 requests / 24 hours
PER USER
4000 requests / 24 hours
PER APP	200 requests / 15 mins
PER USER
2500 requests / 24 hours
PER APP	
GET /2/dm_conversations/:dm_conversation_id/dm_events	15 requests / 15 mins
PER USER	1 requests / 24 hours
PER USER	
GET /2/dm_conversations/with/:participant_id/dm_events	15 requests / 15 mins
PER USER	1 requests / 24 hours
PER USER	
GET /2/dm_events	15 requests / 15 mins
PER USER	1 requests / 24 hours
PER USER	
GET /2/dm_events/:id	15 requests / 15 mins
PER USER	5 requests / 24 hours
PER USER	
POST /2/dm_conversations	15 requests / 15 mins
PER USER
1440 requests / 24 hours
PER APP	1 requests / 24 hours
PER USER
1 requests / 24 hours
PER APP	
POST /2/dm_conversations/:dm_conversation_id/messages	15 requests / 15 mins
PER USER
1440 requests / 24 hours
PER APP	1 requests / 24 hours
PER USER
1 requests / 24 hours
PER APP	
POST /2/dm_conversations/with/:participant_id/messages	1440 requests / 24 hours
PER USER
1440 requests / 24 hours
PER APP	1 requests / 24 hours
PER USER
1 requests / 24 hours
PER APP	
Lists
DELETE /2/lists/:id	300 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
DELETE /2/lists/:id/members/:user_id	300 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
DELETE /2/users/:id/followed_lists/:list_id	50 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
DELETE /2/users/:id/pinned_lists/:list_id	50 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
GET /2/lists/:id	75 requests / 15 mins
PER USER
75 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
5 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/lists/:id/members	900 requests / 15 mins
PER USER
900 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
25 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/lists/:id/tweets	900 requests / 15 mins
PER USER
900 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
25 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/users/:id/list_memberships	75 requests / 15 mins
PER USER
75 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
25 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/users/:id/owned_lists	15 requests / 15 mins
PER USER
15 requests / 15 mins
PER APP	100 requests / 24 hours
PER USER
500 requests / 24 hours
PER APP	1 requests / 24 hours
PER USER
1 requests / 24 hours
PER APP	
GET /2/users/:id/pinned_lists	15 requests / 15 mins
PER USER
15 requests / 15 mins
PER APP	100 requests / 24 hours
PER USER
500 requests / 24 hours
PER APP	1 requests / 24 hours
PER USER
1 requests / 24 hours
PER APP	
POST /2/lists	300 requests / 15 mins
PER USER	100 requests / 24 hours
PER USER	1 requests / 24 hours
PER USER	
POST /2/lists/:id/members	300 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
POST /2/users/:id/followed_lists	50 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
POST /2/users/:id/pinned_lists	50 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
PUT /2/lists/:id	300 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
Bookmarks
DELETE /2/users/:id/bookmarks/:tweet_id	50 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
GET /2/users/:id/bookmarks	180 requests / 15 mins
PER USER	10 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
GET /2/users/:id/bookmarks/folders	50 requests / 15 mins
PER USER
50 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
5 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/users/:id/bookmarks/folders/:folder_id	50 requests / 15 mins
PER USER
50 requests / 15 mins
PER APP	5 requests / 15 mins
PER USER
5 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
POST /2/users/:id/bookmarks	50 requests / 15 mins
PER USER	5 requests / 15 mins
PER USER	1 requests / 15 mins
PER USER	
Compliance
GET /2/compliance/jobs	150 requests / 15 mins
PER APP	5 requests / 15 mins
PER APP	1 requests / 15 mins
PER APP	
GET /2/compliance/jobs/:job_id	150 requests / 15 mins
PER APP	5 requests / 15 mins
PER APP	1 requests / 15 mins
PER APP	
POST /2/compliance/jobs	150 requests / 15 mins
PER APP	15 requests / 15 mins
PER APP	1 requests / 15 mins
PER APP	
Usage
GET /2/usage/tweets	50 requests / 15 mins
PER APP	50 requests / 15 mins
PER APP	1 requests / 15 mins
PER APP	
Trends
GET /2/trends/by/woeid/:id	75 requests / 15 mins
PER APP	15 requests / 15 mins
PER APP	
GET /2/users/personalized_trends	10 requests / 15 mins
PER USER
200 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
20 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 24 hours
PER APP	
Communities
GET /2/communities/:id	300 requests / 15 mins
PER USER
300 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
25 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
GET /2/communities/search	300 requests / 15 mins
PER USER
300 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
25 requests / 15 mins
PER APP	1 requests / 15 mins
PER USER
1 requests / 15 mins
PER APP	
100 results per response
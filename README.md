## Create an API to analyse sentiments and make recommendations from a chat database

### Project goals
The goal of this project is to create an API to get and post info in a database containing data about chats. Among 
To achieve this goal, the following objectives will be pursued:
- Create an API in Flask to store chat messages in MongoDB.
- Extract sentiment from chat messages and perform a report over a whole conversation
- Recommend friends to a user based on the contents from chat messages using a recommender system with `NLP` analysis.
- Deploy the service with docker to heroku and store messages in a cloud database. 

### Tools & Approach
1. Generate a database in Mongo to store chat messages. The database will contain three collections: "users", "chats" and "messages".
- Collection `users`. This collection will store documents about chat users, such as user name and chats which user participates in. Chats will be store as arrays containing references that point to a document in the "chats" collection through the "object ID".
- Collection `chats`. It will store documents about chats added to the database, such as chat name and users in the chat. In the same way that in the previous collection, users will be store as arrays containing references to the "users" collection.
- Collection `messages`. All messages of chat users added to the database will be stored as documents in this collection. In addition to the text, sending date and time of each message, origin user and chat will be stored in the document. Chats and users will be added as references to their corresponding collections. 

2. Create an API in Flask to store users/chats/messages in the database and implement the following endpoints:
- `/user/create/<username>` --> Create a new user and save into DB. This request will receive the "username" parameter and return the object ID.
- `/chat/create` --> Create a new chat. It will receive an user ID (optional) who will participate in the chat and return the chat object ID.
- `/user/<username>` --> Get user ID from a received user name.
- `/chat/<chatname>` --> Get chat ID from a received chat name.
- `/chat/<chat_id>/adduser` --> It will receive the new user to add to an existing chat and return the chat object ID.
- `/chat/<chat_id>/addmessage` --> This request will add a message to an existing chat from an existing user. It will receive the chat ID , user ID, text and sending date-time and returns the messje object ID.
- `/chat/<chat_id>/list` -->  Get all messages from a chat, receiving the chat ID and returning a json array with its content.
- `/user/<user_id>/recommend` --> Recommend friend to this user based on chat contents through NLP analysis. The top 3 of similar users will be returned from the ID user received.
- `/chat/<chat_id>/sentiment` --> Analyze sentiments from chat messages using NLTK package. A json array with all sentiments from messages in the chat will be received.

3. Store messages in Mongo Atlas (cloud database) and create a Docker image with the code to deploy the service to heroku.

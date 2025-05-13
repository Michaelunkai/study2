 Create Microservices Using Node.js
We will create two services:

Service A (Publisher): Publishes messages.
Service B (Subscriber): Listens and processes messages.
3.1. Create Service A (Publisher)
Step 1: Create the Project Folder and Initialize
 
 
mkdir ~/service-a
cd ~/service-a
npm init -y
Step 2: Install Dependencies
Install express and axios for the microservice:

 
 
npm install express axios
Step 3: Create the Publisher Code
Create the main application file:

 
 
nano index.js
Add the following code:

javascript
 
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

const PORT = 3000;
const DAPR_HTTP_PORT = process.env.DAPR_HTTP_PORT || 3500;

app.post('/publish', async (req, res) => {
    const message = req.body.message;
    try {
        await axios.post(`http://localhost:${DAPR_HTTP_PORT}/v1.0/publish/redis-pubsub/messages`, {
            data: message
        });
        res.status(200).send('Message published');
    } catch (error) {
        console.error('Error publishing message:', error);
        res.status(500).send('Error publishing message');
    }
});

app.listen(PORT, () => {
    console.log(`Publisher Service A listening on port ${PORT}`);
});
Make sure the pubsubname in the URL (redis-pubsub) matches the component name.

3.2. Create Service B (Subscriber)
Step 1: Create the Project Folder and Initialize
In the same directory as service-a, create a new service:

 
 
mkdir ~/service-b
cd ~/service-b
npm init -y
Step 2: Install Dependencies
Install express:

 
 
npm install express
Step 3: Create the Subscriber Code
Create the main application file:

 
 
nano index.js
Add the following code:

javascript
 
const express = require('express');

const app = express();
app.use(express.json());

const PORT = 4000;

app.post('/messages', (req, res) => {
    const message = req.body.data;
    console.log('Received message:', message);
    res.status(200).send('Message received');
});

app.listen(PORT, () => {
    console.log(`Subscriber Service B listening on port ${PORT}`);
});

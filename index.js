// Example express application adding the parse-server module to expose Parse
// compatible API routes.

import express from 'express';
import { ParseServer } from 'parse-server';
import path from 'path';
const __dirname = path.resolve();
import http from 'http';
import dotenv from 'dotenv';
import cors from 'cors';

dotenv.config();

export const config = {
  databaseURI: process.env.MONGODB_URI,
  cloud: process.env.CLOUD_CODE_MAIN,
  appId: process.env.APP_ID,
  masterKey: process.env.MASTER_KEY,
  serverURL: process.env.SERVER_URL,
  restAPIKey: process.env.REST_API_KEY,
  liveQuery: {
    classNames: ['Posts', 'Comments'], // List of classes to support for query subscriptions
  },
  allowClientClassCreation: true,
  allowExpiredAuthDataToken: true,
  encodeParseObjectInCloudFunction: true
};

export const app = express();
app.use(cors()); 

// Logging middleware
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} Request to ${req.url}`);
  next();
});


// Serve the Parse API on the /parse URL prefix
if (!process.env.TESTING) {
  const mountPath = process.env.PARSE_MOUNT || '/parse';
  const server = new ParseServer(config);
  await server.start();
  app.use(mountPath, server.app);
}

// Parse Server plays nicely with the rest of your web routes
app.get('/', function (req, res) {
  res.status(200).send('FMD API Server');
});


if (!process.env.TESTING) {
  const port = process.env.PORT || 4000;
  const httpServer = http.createServer(app);
  httpServer.listen(port, '0.0.0.0', function() {
    console.log('fmd-server running on port ' + port + '.');
  });
  
  // This will enable the Live Query real-time server
  await ParseServer.createLiveQueryServer(httpServer);
}

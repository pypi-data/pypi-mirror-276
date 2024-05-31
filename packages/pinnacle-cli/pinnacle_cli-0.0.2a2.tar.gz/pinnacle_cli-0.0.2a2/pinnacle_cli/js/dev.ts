import express from "express";
const fs = require("fs");
const path = require("path");
const constants = require("./constants");
const app = express();
const cors = require("cors");
app.use(cors());
app.use(express.json());

const cwd = process.argv[2];

const pinnacleDirectory = `${cwd}/${constants.DIRECTORY}`;
const files = fs.readdirSync(pinnacleDirectory);

files.forEach((file: string) => {
  const ext = path.extname(file);
  if (ext === ".js" || ext === ".ts") {
    const functionModule = require(path.join(pinnacleDirectory, file));
    const functions = Object.getOwnPropertyNames(functionModule).filter(
      (prop) => typeof functionModule[prop] === "function"
    );


    functions.forEach((func) => {
      const callableFunction = functionModule[func];
      console.log(`http://${constants.HOST}:${constants.JAVASCRIPT_PORT}/${func}`);
      app.post(`/${func}`, (req: express.Request, res: express.Response) => { // Explicitly define the types for req and res
        const result = callableFunction(...Object.entries(req.body));
        res.send({ data: result });
      });
    });
  }
});

app.listen(constants.JAVASCRIPT_PORT);

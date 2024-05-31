require("dotenv").config();

const HOST = process.env.PINNACLE_HOST || "localhost";
const PORT = Number(process.env.PINNACLE_PORT) || 8000;
const DIRECTORY = process.env.PINNACLE_DIRECTORY || "./pinnacle";
const JAVASCRIPT_PORT = PORT + 2;

module.exports = {
  HOST,
  PORT,
  DIRECTORY,
  JAVASCRIPT_PORT,
};

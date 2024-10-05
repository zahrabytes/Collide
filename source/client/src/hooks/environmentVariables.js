const SERVER_BASE_ENDPOINT = process.env.REACT_APP_SERVER_BASE_ENDPOINT;
const USE_MOCK_DATA = ["1", "true", "t", "yes", "y"].includes(
  process.env.REACT_APP_USE_MOCK_DATA.toLowerCase()
);

export { SERVER_BASE_ENDPOINT, USE_MOCK_DATA };

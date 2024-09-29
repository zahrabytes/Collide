import { useEffect, useState } from "react";
import { SERVER_BASE_ENDPOINT } from "./getServerBaseEndpoint";

function useTrendingTopics() {
  const endpoint = `${SERVER_BASE_ENDPOINT}/trendingtopics`;
  const [topics, setTopics] = useState([]);
  useEffect(() => {
    fetch(endpoint)
      .then((response) => response.json())
      .then((newTopics) => setTopics(newTopics));
  }, []);
  return topics;
}

export { useTrendingTopics };

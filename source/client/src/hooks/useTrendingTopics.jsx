import { useEffect, useState } from "react";
import { SERVER_BASE_ENDPOINT, USE_MOCK_DATA } from "./environmentVariables";

import mockTopics from "../assets/json/mockTrendingTopics.json";

function useTrendingTopics() {
  const endpoint = `${SERVER_BASE_ENDPOINT}/trendingtopics`;
  const [topics, setTopics] = useState([]);

  useEffect(() => {
    if (USE_MOCK_DATA) {
      setTopics(mockTopics);
    } else {
      fetch(endpoint)
        .then((response) => response.json())
        .then((newTopics) => setTopics(newTopics));
    }
  }, [endpoint]);

  return topics;
}

export { useTrendingTopics };

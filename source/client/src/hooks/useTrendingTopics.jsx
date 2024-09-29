import { useEffect, useState } from "react";

const baseEndpoint = "http://127.0.0.1:5000";

function useTrendingTopics(userId) {
  const endpoint = `${baseEndpoint}/trendingTopics`;
  const [topics, setTopics] = useState([]);
  useEffect(() => {
    fetch(endpoint)
      .then((response) => response.json())
      .then((newTopics) => setTopics(newTopics));
  }, []);
  return topics;
}

export { useTrendingTopics };

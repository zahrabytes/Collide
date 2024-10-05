import { useEffect, useState } from "react";
import { SERVER_BASE_ENDPOINT, USE_MOCK_DATA } from "./environmentVariables";

import mockPosts from "../assets/json/mockPosts.json";

function useRecommendedPosts(userId) {
  const endpoint = `${SERVER_BASE_ENDPOINT}/user/${userId}/recommendedposts`;
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    if (USE_MOCK_DATA) {
      setPosts(mockPosts);
    } else {
      fetch(endpoint)
        .then((response) => response.json())
        .then((data) => data.posts)
        .then((posts) => setPosts(posts));
    }
  }, [endpoint]);

  return posts;
}

export { useRecommendedPosts };

import { useEffect, useState } from "react";
import { SERVER_BASE_ENDPOINT } from "./getServerBaseEndpoint";

function useRecommendedPosts(userId) {
  const endpoint = `${SERVER_BASE_ENDPOINT}/users/${userId}/recommendedposts`;
  const [posts, setPosts] = useState([]);
  useEffect(() => {
    fetch(endpoint)
      .then((response) => response.json())
      .then((data) => data.posts)
      .then((posts) => setPosts(posts));
  }, []);
  return posts;
}

export { useRecommendedPosts };

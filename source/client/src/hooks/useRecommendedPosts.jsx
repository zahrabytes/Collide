import { useEffect, useState } from "react";

const baseEndpoint = "http://127.0.0.1:5000";

function useRecommendedPosts(userId) {
  const endpoint = `${baseEndpoint}/users/${userId}/recommendedPosts`;
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

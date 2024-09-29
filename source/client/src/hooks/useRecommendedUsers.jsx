import { useEffect, useState } from "react";

const baseEndpoint = "http://127.0.0.1:5000";

function useRecommendedUsers(userId) {
  const endpoint = `${baseEndpoint}/users/${userId}/recommendedusers`;
  const [users, setUsers] = useState([]);
  useEffect(() => {
    fetch(endpoint)
      .then((response) => response.json())
      .then((posts) => setUsers(posts));
  }, []);
  return users;
}

export { useRecommendedUsers };

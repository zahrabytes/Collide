import { useEffect, useState } from "react";
import { SERVER_BASE_ENDPOINT } from "./getServerBaseEndpoint";

function useRecommendedUsers(userId) {
  const endpoint = `${SERVER_BASE_ENDPOINT}/user/${userId}/recommendedusers`;
  const [users, setUsers] = useState([]);
  useEffect(() => {
    fetch(endpoint)
      .then((response) => response.json())
      .then((posts) => setUsers(posts));
  }, []);
  return users;
}

export { useRecommendedUsers };

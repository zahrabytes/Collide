import { useEffect, useState } from "react";
import { SERVER_BASE_ENDPOINT, USE_MOCK_DATA } from "./environmentVariables";

import mockUsers from "../assets/json/mockUsers.json";

function useRecommendedUsers(userId) {
  const endpoint = `${SERVER_BASE_ENDPOINT}/user/${userId}/recommendedusers`;
  const [users, setUsers] = useState([]);

  useEffect(() => {
    if (USE_MOCK_DATA) {
      setUsers(mockUsers);
    } else {
      fetch(endpoint)
        .then((response) => response.json())
        .then((posts) => setUsers(posts));
    }
  }, [endpoint]);

  return users;
}

export { useRecommendedUsers };

import { useEffect, useState } from "react";
import { SERVER_BASE_ENDPOINT, USE_MOCK_DATA } from "./environmentVariables";

import mockUsers from "../assets/json/mockUsers.json";

function useUser(userId) {
  const endpoint = `${SERVER_BASE_ENDPOINT}/user/${userId}`;
  const [user, setUser] = useState([]);

  useEffect(() => {
    if (USE_MOCK_DATA) {
      const user = mockUsers.find((user) => user.id === parseInt(userId));
      setUser(user);
    } else {
      fetch(endpoint)
        .then((response) => response.json())
        .then((newUser) => setUser(newUser));
    }
  }, [endpoint, userId]);

  return user;
}

export { useUser };

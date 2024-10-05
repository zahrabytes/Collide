import { useEffect, useState } from "react";
import { SERVER_BASE_ENDPOINT, USE_MOCK_DATA } from "./environmentVariables";

import mockUsers from "../assets/json/mockUsers.json";

function useUsers() {
  const endpoint = `${SERVER_BASE_ENDPOINT}/users`;
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (USE_MOCK_DATA) {
      setUsers(mockUsers);
    } else {
      fetch(endpoint)
        .then((response) => response.json())
        .then((data) => setUsers(data.users || data))
        .catch((error) => setError(error));
    }
    setLoading(false);
  }, [endpoint]);

  return { users, loading, error };
}

export { useUsers };

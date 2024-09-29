import { useEffect, useState } from "react";
import { SERVER_BASE_ENDPOINT } from "./getServerBaseEndpoint";

function useUser(userId) {
  const endpoint = `${SERVER_BASE_ENDPOINT}/user/${userId}`;
  const [user, setUser] = useState([]);
  useEffect(() => {
    fetch(endpoint)
      .then((response) => response.json())
      .then((newUser) => setUser(newUser));
  }, []);
  return user;
}

export { useUser };

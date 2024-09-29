import { useEffect, useState } from "react";

const baseEndpoint = "http://127.0.0.1:5000";

function useUser(userId) {
  const endpoint = `${baseEndpoint}/user/${userId}`;
  const [user, setUser] = useState([]);
  useEffect(() => {
    fetch(endpoint)
      .then((response) => response.json())
      .then((newUser) => setUser(newUser));
  }, []);
  return user;
}

export { useUser };

import { useEffect, useState } from "react";

function useFetchUsers(amount) {
  const [users, setUsers] = useState([]);
  useEffect(() => {
    const getUsers = async (amount) => {
      const fetchRequests = Array.from({ length: amount }).map(() =>
        fetch("https://randomuser.me/api")
          .then((response) => response.json())
          .then((json) => json.results[0])
      );
      const users = await Promise.all(fetchRequests);
      return users;
    };
    getUsers(amount).then((users) => {
      setUsers(users);
    });
  }, [amount]);
  return users;
}

export { useFetchUsers };

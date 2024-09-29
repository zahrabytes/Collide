// import { useEffect, useState, useMemo } from "react";

// const fetchSingleUser = () => {
//   return fetch("https://randomuser.me/api")
//     .then((response) => response.json())
//     .then((json) => json.results[0]);
// };

// const fetchUsersList = async (amount) => {
//   const fetchRequests = Array.from({ length: amount }).map(() =>
//     fetchSingleUser()
//   );
//   const users = await Promise.all(fetchRequests);
//   return users;
// };

// function useFetchUsers(amount) {
//   const [users, setUsers] = useState([]);

//   const fetchUsers = useMemo(() => fetchUsersList, []);

//   useEffect(() => {
//     fetchUsers(amount).then((fetchedUsers) => {
//       setUsers(fetchedUsers);
//     });
//   }, [amount, fetchUsers]);

//   return users;
// }

// export { useFetchUsers };

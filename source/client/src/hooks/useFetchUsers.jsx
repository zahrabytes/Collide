import { useEffect, useState, useMemo } from "react";

// Fetch a single user by ID from the provided API
const fetchSingleUser = (userId) => {
  return fetch(`http://127.0.0.1:5000/user/${userId}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Failed to fetch user with ID ${userId}`);
      }
      return response.json();
    })
    .then((json) => json); // Assuming the API returns a single user object
};

// Fetch a list of users based on an array of user IDs
const fetchUsersList = async (userIds) => {
  const fetchRequests = userIds.map((userId) => fetchSingleUser(userId)); // Fetch each user by ID
  const users = await Promise.all(fetchRequests); // Wait for all requests to complete
  return users; // Return the array of users
};

// Custom hook to fetch a list of users by their IDs
function useFetchUsers(userIds) {
  const [users, setUsers] = useState([]); // State to store fetched users

  const fetchUsers = useMemo(() => fetchUsersList, []); // Memoize the fetch function to avoid re-creating it on every render

  useEffect(() => {
    if (userIds && userIds.length > 0) {
      fetchUsers(userIds).then((fetchedUsers) => {
        setUsers(fetchedUsers); // Set the fetched users in state
      }).catch((error) => {
        console.error("Error fetching users:", error); // Handle any errors during fetching
      });
    }
  }, [userIds, fetchUsers]); // Only re-fetch when user IDs change

  return users; // Return the users array
}

export { useFetchUsers };

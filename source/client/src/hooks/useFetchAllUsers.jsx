import { useEffect, useState } from "react";
import { SERVER_BASE_ENDPOINT } from "./getServerBaseEndpoint";

function useFetchAllUsers() {
  const endpoint = `${SERVER_BASE_ENDPOINT}/users`; // URL to fetch all users
  const [users, setUsers] = useState([]); // State to hold users data
  const [loading, setLoading] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch(endpoint, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        // Check if the response is OK (status 200-299)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json(); // Wait for the JSON conversion
        console.log("API response:", data); // Log the full API response

        setUsers(data.users || data); // Assuming the response contains an array or a 'users' field
      } catch (err) {
        console.error("Fetch error:", err); // Log any errors
        setError(err.message); // Handle the error
      } finally {
        setLoading(false); // Stop loading
      }
    };

    // Call the async function
    fetchUsers();
  }, [endpoint]); // Only fetch users when the component mounts

  return { users, loading, error };
}

export { useFetchAllUsers };

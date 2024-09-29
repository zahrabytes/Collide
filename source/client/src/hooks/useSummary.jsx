import { useEffect, useState } from "react";

const baseEndpoint = "http://127.0.0.1:5000";

function useSummary(userId) {
  const endpoint = `${baseEndpoint}/user/${userId}/summary`;
  const [summary, setSummary] = useState([]);
  useEffect(() => {
    fetch(endpoint)
      .then((response) => response.json())
      .then((posts) => setSummary(posts));
  }, []);
  return summary;
}

export { useSummary };

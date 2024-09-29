import { useEffect, useState } from "react";
import { SERVER_BASE_ENDPOINT } from "./getServerBaseEndpoint";

function useSummary(userId) {
  const endpoint = `${SERVER_BASE_ENDPOINT}/user/${userId}/summary`;
  const [summary, setSummary] = useState([]);
  useEffect(() => {
    fetch(endpoint)
      .then((response) => response.json())
      .then((posts) => setSummary(posts));
  }, []);
  return summary;
}

export { useSummary };

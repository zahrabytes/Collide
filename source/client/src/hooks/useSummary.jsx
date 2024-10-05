import { useEffect, useState } from "react";
import { SERVER_BASE_ENDPOINT, USE_MOCK_DATA } from "./environmentVariables";

import mockSummary from "../assets/json/mockSummary.json";

function useSummary(userId) {
  const endpoint = `${SERVER_BASE_ENDPOINT}/user/${userId}/summary`;
  const [summary, setSummary] = useState([]);

  useEffect(() => {
    if (USE_MOCK_DATA) {
      setSummary(mockSummary);
    } else {
      fetch(endpoint)
        .then((response) => response.json())
        .then((newSummary) => setSummary(newSummary));
    }
  }, [endpoint]);

  return summary;
}

export { useSummary };

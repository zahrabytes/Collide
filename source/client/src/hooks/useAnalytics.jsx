import { useEffect, useState } from "react";
import { SERVER_BASE_ENDPOINT, USE_MOCK_DATA } from "./environmentVariables";

import mockAnalytics from "../assets/json/mockAnalytics.json";

function useAnalytics(userId, topics) {
  const endpointTopicsMatch = `${SERVER_BASE_ENDPOINT}/user/${userId}/analytics/topicsmatch/${topics}`;
  const endpointInterests = `${SERVER_BASE_ENDPOINT}/user/${userId}/analytics/interests`;

  const [topicsMatch, setTopicsMatch] = useState({});
  const [interests, setInterests] = useState({});

  useEffect(() => {
    if (USE_MOCK_DATA) {
      setTopicsMatch(mockAnalytics.topicsMatch);
      setInterests(mockAnalytics.interests);
    } else {
      Promise.all([fetch(endpointTopicsMatch), fetch(endpointInterests)])
        .then(([res1, res2]) => {
          return Promise.all([res1.json(), res2.json()]);
        })
        .then(([newTopicsMatch, newInterests]) => {
          setTopicsMatch(newTopicsMatch);
          setInterests(newInterests);
        })
        .catch((err) => {
          setTopicsMatch({});
          setInterests({});
          console.error(err);
        });
    }
  }, [endpointTopicsMatch, endpointInterests]);

  return { topicsMatch, interests };
}

export { useAnalytics };

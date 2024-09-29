import { useEffect, useState } from "react";
import { SERVER_BASE_ENDPOINT } from "./getServerBaseEndpoint";

function useAnalytics(userId, topics) {
  const endpointTopicsMatch = `${SERVER_BASE_ENDPOINT}/user/${userId}/analytics/topicsmatch/${topics}`;
  const endpointInterests = `${SERVER_BASE_ENDPOINT}/user/${userId}/analytics/interests`;

  const [topicsMatch, setTopicsMatch] = useState({});
  const [interests, setInterests] = useState({});

  useEffect(() => {
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
  }, [endpointTopicsMatch, endpointInterests]);

  return { topicsMatch, interests };
}

export { useAnalytics };

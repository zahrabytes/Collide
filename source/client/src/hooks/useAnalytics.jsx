import { useEffect, useState } from "react";

const baseEndpoint = "http://127.0.0.1:5000";

function useAnalytics(userId, topics) {
  topics = "HydrogenInvestmentInfrastructureAcquisition";
  const endpointTopicsMatch = `${baseEndpoint}/user/${userId}/analytics/topicsmatch/${topics}`;
  const endpointInterests = `${baseEndpoint}/user/${userId}/analytics/interests`;

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
      });
  }, []);

  return { topicsMatch, interests };
}

export { useAnalytics };

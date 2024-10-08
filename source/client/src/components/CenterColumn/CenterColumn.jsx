import { useState } from "react";
import { useAnalytics } from "../../hooks/useAnalytics";
import { useRecommendedPosts } from "../../hooks/useRecommendedPosts";
import { useSummary } from "../../hooks/useSummary";
import { useUser } from "../../hooks/useUser";
import { Analytics } from "../Analytics/Analytics";
import { Posts } from "../Posts/Posts";
import { Summary } from "../Summary/Summary";
import styles from "./CenterColumn.module.scss";

function CenterColumn({ userId, trendingTopics }) {
  const [selectedPage, setselectedPage] = useState("suggested");
  const updateSelectedPage = (page) => {
    return () => setselectedPage(page);
  };

  const posts = useRecommendedPosts(userId);
  const user = useUser(userId);

  const analytics = useAnalytics(userId, trendingTopics.slice(0, 10).join(""));

  const summary = useSummary(userId);

  return (
    <div className={styles.container}>
      <div className={styles.chips}>
        <div className={styles.green} onClick={updateSelectedPage("suggested")}>
          Suggested
        </div>
        <div className={styles.blue} onClick={updateSelectedPage("analytics")}>
          Analytics
        </div>
        <div className={styles.orange} onClick={updateSelectedPage("summary")}>
          Summary
        </div>
      </div>
      {selectedPage === "suggested" && <Posts {...{ posts, user }} />}
      {selectedPage === "analytics" && <Analytics analytics={analytics} />}
      {selectedPage === "summary" && <Summary summary={summary} />}
    </div>
  );
}

export { CenterColumn };
